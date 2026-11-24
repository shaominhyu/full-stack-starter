# 项目索引

本仓库基于 Full Stack FastAPI Template，包含 FastAPI、React、PostgreSQL 和 Docker Compose。

| 任务 | 入口 |
| --- | --- |
| 接手任务，查找已有经验、现行流程或待核实的变化 | [项目脉络](context/README.md) |
| 启动、停止、排查本地服务、查看数据库或了解发布流程 | [运维手册](docs/operations.md) |
| 查看项目功能和技术栈 | [项目 README](README.md) |
| 修改 API、数据库模型或迁移 | [后端说明](backend/README.md) |
| 修改页面、生成 API 客户端或运行浏览器测试 | [前端说明](frontend/README.md) |
| 创建或复用 worktree、命名分支、写提交信息和 PR/MR | [Worktree 开发流程](docs/worktree-workflow.md) |
| 提交前跑测试、检查代码复用 | [质量检查](docs/quality-checks.md) |

开始修改源码前，先读取 `docs/worktree-workflow.md`，从最新的 `origin/develop` 创建或复用 `feat/*` worktree。日常改动通过 PR 合入 `develop`。生产发布通过 `develop → master` 的 PR 进行。主工作目录用于运行项目、排查和同步分支。

用户说「启动项目」时，在主工作目录按运维手册启动本地开发环境。先检查现有服务，复用已运行的实例。启动后验证页面和 API，向用户报告访问地址及实际验证结果。

修改源码后，按质量检查文档执行受影响的测试和重复代码检查，报告实际命令、结果和未验证项。功能测试使用隔离测试脚本创建的测试环境。新增实现前先查找已有调用点，核对输入、权限和事务行为后再决定是否复用。

接手任务时先查项目脉络索引。命中已有主题或收到相关新资料时，按[维护约定](context/maintenance.md)核对依据，复用适用的结论，并自动维护受影响的条目。发现替换或尚未解决的冲突时，在本次回复里提醒用户。新主题由用户主动选择沉淀。
