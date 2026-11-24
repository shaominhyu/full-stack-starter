# 这个项目怎样发布到测试或生产环境？

推送到 `develop` 或 `master` 后会运行集成检查。部署需从 GitHub Actions 手动发起。先确认目标环境，再查看准备发布的提交上的工作流和手册。

| 目标 | 在 Actions 中选择 | 运行条件 |
| --- | --- | --- |
| 自托管测试环境 | 在 `develop` 手动运行 **Deploy with Docker Compose** | `TESTING_COMPOSE_DEPLOY_ENABLED=true`，目标服务器的 Runner 带有 `fullstack-testing` 标签。 |
| 自托管生产环境 | 将通过测试的 `develop` 版本经发布 PR 合入 `master`，在 `master` 手动运行 **Deploy with Docker Compose** | `PRODUCTION_COMPOSE_DEPLOY_ENABLED=true`，目标服务器的 Runner 带有 `fullstack-production` 标签。 |
| FastAPI Cloud 生产环境 | 发布 PR 合入 `master` 后，在该分支手动运行 **Deploy** | 已配置应用、生产数据库与部署凭据，并设置 `PRODUCTION_CLOUD_DEPLOY_ENABLED=true`。 |

本地启动开发服务见运维手册。查生产部署时以实际选中分支的配置为准，`develop` 上的工作流改动要经发布 PR 才会进入 `master`。部署后核对运行记录上的分支、提交和结果，再访问目标环境的应用及其 `/docs`。如果合并后没看到 Cloud 发布记录，先查[触发条件的变更经过](../questions/cloud-deploy-trigger.md)。

## 核对来源

- [运维手册的环境与发布入口](operations.md#生产部署和-cicd)
- [FastAPI Cloud 部署手册](../../deployment.md#configure-continuous-deployment)
- [Cloud 发布工作流](../../.github/workflows/deploy.yml)
- [自托管 Compose 部署手册](../../deployment-docker-compose.md#deploy-with-github-actions)
- [自托管发布工作流](../../.github/workflows/deploy-docker-compose.yml)
