# 怎样提任务 PR 和发布 PR？

适用于 `shaominhyu/full-stack-starter`。准备提 MR、选择目标分支或排查 `check-branch-flow` 失败时，先确认 PR 的用途。

| 用途 | 源分支 → 目标分支 | 提交前核对 | 合并方式 |
| --- | --- | --- | --- |
| 日常任务 | 同仓库的 `feat/<任务短名> → develop` | 复用已有任务工作树，新建时从最新的 `origin/develop` 开始。运行改动涉及的检查，重复代码检查以 `origin/develop` 为基线。 | Squash and merge |
| 生产发布 | 同仓库的 `develop → master` | 确认待发布版本已经在测试环境通过验证。发布 PR 的重复代码检查以 `origin/master` 为基线。 | Create a merge commit |

提交首行和 PR 标题用 `type(scope): summary`，范围可省略。任务分支推送到 `origin` 后，在 PR 正文说明改动原因、内容、实际检查结果及未验证项。

当 **Branch flow** 报错时，在 PR 页面核对源仓库、源分支和目标分支。两条路径都要求源分支属于本仓库。分支策略或质量检查要求有变时，重新核对上表。

## 核对来源

- [工作树、分支和合并约定](../../docs/worktree-workflow.md) <!-- sha256:7772cf31bb6b86a5e2eee878edb1914966e2cfe0cf8b4d30d221aef1a1bfaadb -->
- [提交前的质量检查](../../docs/quality-checks.md) <!-- sha256:a15ed6504070ea24c11f3e5fc4c783040bc2565a6e960fd49faf4f075f34d743 -->
- [PR 源分支与目标分支检查](../../.github/workflows/check-branch-flow.yml) <!-- sha256:b89c233122fac71aaa174aae0a94db3456891768c3e0d14a18d4f58c56918ce9 -->
