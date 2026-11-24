import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "check.py"


class ContextCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "project"
        self.context = self.root / "context"
        self.guide = self.context / "guides" / "部署.md"
        self.guide.parent.mkdir(parents=True)
        self.script = self.context / "check.py"
        shutil.copyfile(CHECKER, self.script)
        self.source = self.root / "手册.md"
        self.source.write_text("旧流程\n", encoding="utf-8")
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.reference = f"- [手册](../../手册.md#部署) <!-- sha256:{digest} -->"

    def run_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script)],
            cwd=self.guide.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_no_topics(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 0)
        self.assertIn("0 条", result.stdout)

    def test_verified_reference_ordinary_link_and_code_example(self) -> None:
        self.guide.write_text(
            f"- [其他](missing.md) <!-- 等待编辑 -->\n```md\n{self.reference} 错误示例\n```\n{self.reference}\n",
            encoding="utf-8",
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("1 条", result.stdout)

    def test_changed_source_points_to_each_affected_entry(self) -> None:
        question = self.context / "questions" / "发布.md"
        question.parent.mkdir()
        for page in (self.guide, question):
            page.write_text(self.reference, encoding="utf-8")
        self.source.write_text("新流程\n", encoding="utf-8")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        for kind in ("guides/部署.md", "questions/发布.md"):
            self.assertIn(kind, result.stdout)
        self.assertIn("../../手册.md#部署", result.stdout)
        self.assertEqual(self.guide.read_text(encoding="utf-8"), self.reference)

    def test_missing_source(self) -> None:
        self.guide.write_text(self.reference, encoding="utf-8")
        self.source.unlink()
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("来源缺失", result.stdout)

    def test_malformed_digest_or_marker_is_reported(self) -> None:
        for replacement in ("sha256:short-", "sha265:"):
            with self.subTest(replacement=replacement):
                self.guide.write_text(
                    self.reference.replace("sha256:", replacement), encoding="utf-8"
                )
                result = self.run_check()
                self.assertEqual(result.returncode, 2)
                self.assertIn("格式错误", result.stdout)
                self.assertIn("../../手册.md#部署", result.stdout)

    def test_relative_path_and_symlink_outside_project(self) -> None:
        outside = self.root.parent / "external.md"
        outside.write_text("外部原始内容", encoding="utf-8")
        (self.guide.parent / "link.md").symlink_to(outside)
        for destination in ("../../../external.md", "link.md"):
            with self.subTest(destination=destination):
                self.guide.write_text(
                    self.reference.replace("../../手册.md#部署", destination),
                    encoding="utf-8",
                )
                result = self.run_check()
                self.assertEqual(result.returncode, 2)
                self.assertIn("超出项目目录", result.stdout)
                self.assertIn(destination, result.stdout)
                self.assertNotIn("外部原始内容", result.stdout)
