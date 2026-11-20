# 提交和提 MR 前的检查

从仓库根目录执行。按本次改动选相关命令。前后端都改了就跑两边。执行后记录测试命令、实际结果和未验证项。

| 改动 | 本地命令 | 验证内容 |
| --- | --- | --- |
| 后端 API、业务规则或权限 | `bash scripts/test-isolated.sh backend tests/api/routes/test_items.py` | 直接请求 API，检查数据和权限。将路径换成对应的 Pytest 文件，省略路径运行后端全套。 |
| 前端交互或跨前后端的功能 | `bash scripts/test-isolated.sh browser tests/items.spec.ts` | 用浏览器跑用户操作，确认能提交并看到结果。将路径换成对应的用例，省略路径运行 Playwright 全套。 |
| Dockerfile、Compose 或数据库迁移 | `bash scripts/test-isolated.sh compose` | 构建应用镜像、迁移空数据库、访问 API 健康检查和登录页。迁移改动还要跑受影响的后端测试。 |
| 修改 Python 代码 | `(cd backend && uv run --locked bash scripts/lint.sh)` | 检查 Python 类型、lint 和格式。 |
| 修改前端代码 | `(cd frontend && bun run build)` | 用 TypeScript 检查类型，再构建前端。需要已安装前端依赖。 |
| 修改应用源码或复用规则 | `bash scripts/check-duplication.sh origin/master` | 以 MR 目标分支为基线，检查新增重复和违反复用规则的代码。按实际目标分支替换 `origin/master`。 |

## 测试环境

隔离脚本需要 Docker Compose 2.24.4 或更高版本。后端测试还需要 `uv`。脚本为每次运行创建独立的 `fullstack-test-*` Compose 项目和数据库卷，结束后清理该测试项目。首次跑浏览器或 Compose 检查时需要下载镜像并构建应用。Pytest 会删除测试库中的 `item` 和 `user` 记录，日常开发库用 `fullstack-local` 继续访问。

## 防重复代码

- **jscpd** 比较整个 `backend/app` 和 `frontend/src` 中的 Python、JS 和 TS 源码，排除生成的 API 客户端和路由树。报告中的 `[NEW]` 表示相对于目标提交新增的重复。修正时查看报告的两处位置，优先调用已有实现。
- **ast-grep** 执行可测试的项目规则。当前规则要求 API 路由通过 `crud.create_item()` 创建条目，并验证委派调用、普通查找和直接构造等样例。新增规则时，同步添加应通过和应拦截的样例。

重复检查需要 Node.js 和 npm。首次执行时，脚本通过 npm 获取固定版本的工具。用 `git fetch origin` 更新本地目标分支引用后，再用同一脚本复现 CI 结果。

GitHub Actions 在 PR 中使用目标提交运行 [重复代码检查](../.github/workflows/check-duplication.yml)。将 `check-duplication` 设为目标分支的必需状态检查后，失败的 PR 会被阻止合并。后端测试、浏览器测试和启动验证沿用仓库已有的工作流。
