# 项目索引

本仓库基于 Full Stack FastAPI Template，包含 FastAPI、React、PostgreSQL 和 Docker Compose。

| 任务 | 入口 |
| --- | --- |
| 启动、停止、排查本地服务、查看数据库或了解发布流程 | [运维手册](docs/operations.md) |
| 查看项目功能和技术栈 | [项目 README](README.md) |
| 修改 API、数据库模型或迁移 | [后端说明](backend/README.md) |
| 修改页面、生成 API 客户端或运行浏览器测试 | [前端说明](frontend/README.md) |
| 提交或提 MR 前跑测试、检查代码复用 | [质量检查](docs/quality-checks.md) |

用户说「启动项目」时，按运维手册启动本地开发环境。先检查现有服务，复用已运行的实例。启动后验证页面和 API，向用户报告访问地址及实际验证结果。

修改源码后，按质量检查文档执行受影响的测试和重复代码检查，报告实际命令、结果和未验证项。功能测试使用隔离测试脚本创建的测试环境。新增实现前先查找已有调用点，核对输入、权限和事务行为后再决定是否复用。
