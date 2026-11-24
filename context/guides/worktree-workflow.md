# Worktree 开发流程

## 分支流向

| 分支 | 用途 |
| --- | --- |
| `feat/*` | 从 `develop` 创建任务分支，完成后提 PR 到 `develop`。 |
| `develop` | 默认分支和日常集成线，也是开发和测试环境的部署来源。 |
| `master` | 生产发布线。准备上线时，从同仓库的 `develop` 提发布 PR。 |

## 分支与目录命名

- 任务分支用 `feat/<任务短名>`，例如 `feat/items-filter` 或 `feat/fix-login-redirect`。
- 工作树放在主目录的 `worktrees/` 下，目录名用 `fullstack-feat-<任务短名>`。
- 任务短名用小写英文和连字符。有 Issue 编号时可放在短名前，例如 `feat/42-login-redirect`。

## 创建或复用工作树

先用 `git worktree list` 查找当前任务的工作树。新任务从最新的 `origin/develop` 创建。

```bash
git fetch origin develop
mkdir -p worktrees
git worktree add -b feat/items-filter worktrees/fullstack-feat-items-filter origin/develop
cd worktrees/fullstack-feat-items-filter
```

主目录的 Git 忽略规则覆盖整个 `worktrees/`，任务改动从对应的工作树里提交。

## 提交信息与 PR/MR 标题

Commit 首行和 PR/MR 标题统一用 `type(scope): summary`。`type` 表明改动类型，`scope` 表明涉及的模块，省略时写 `type: summary`。开发者和 AI 在提交前自行核对格式。[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

常用类型包括 `feat`（新功能）、`fix`（修复）、`docs`（文档）、`refactor`（重构）、`test`（测试）和 `chore`（工程维护）。摘要写清实际改动。

```text
feat(items): add status filter
fix(auth): correct login redirect
docs: update the worktree guide
```

PR/MR 正文写明改动原因、内容和实际验证结果。有相关 Issue 时关联它，在 GitHub 上完整解决该 Issue 时可用 `Closes #42`。 [GitHub 关联 Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)

## 提交和合并

1. 完成[提交前检查](quality-checks.md)，从工作树提交并运行 `git push -u origin HEAD`。
2. 向 `develop` 提任务 PR，使用 **Squash and merge**。确认合入后即可清理任务 worktree。
3. 准备上线时，确认 `develop` 的待发布版本在测试环境通过验证，提 `develop → master` 发布 PR，使用 **Create a merge commit** 保留两条长期分支的合并关系。合并后按[运维手册](operations.md#生产部署和-cicd)发布。

GitHub Actions 的 **Branch flow** 检查会核对 PR 的源分支和目标分支。支持分支保护的仓库可将 `check-branch-flow` 设为 `develop` 和 `master` 的必需检查。

依赖版本由 `feat/*` 任务 PR 更新。Dependabot 的配置示例保存在 `.github/dependabot.yml.example`，可作为后续调整依赖更新流程的参考。
