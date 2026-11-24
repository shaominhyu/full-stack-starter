# 合并后为什么没有看到 FastAPI Cloud 发布？

这条经验适用于本仓库的生产 Cloud 工作流 **Deploy**。查找线索包括「合并后没有发布」「Actions 没有 Deploy 记录」和「手动运行后 deploy 作业被跳过」。

## 下次先查什么

1. **没有运行记录。** 查看目标分支的 `.github/workflows/deploy.yml` 中的 `on`。当前只声明 `workflow_dispatch`，合并任务 PR 或发布 PR 都不会自动创建一条 Cloud 部署记录。需要发布时，按[部署指南](../guides/deployment.md)从 `master` 手动运行。
2. **有运行记录，作业被跳过。** 查看该次运行所选分支以及工作流中作业的 `if` 条件。Cloud 作业要求选择 `master`，且仓库变量 `PRODUCTION_CLOUD_DEPLOY_ENABLED` 的值为 `true`。
3. **作业已开始，随后失败。** 查看失败的具体步骤。构建、准备数据库、上传应用分别留下运行日志，可以据此缩小排查范围。

## 判断如何变化

- 提交 `b516283` 移除了推送到 `master` 时的自动 Cloud 部署触发条件，保留手动入口。等待合并后自动出现运行记录的做法由此失效。[项目变更 b516283](https://github.com/shaominhyu/full-stack-starter/commit/b51628331a6d4a275536b9c83dcef85a0fba48a2)
- 2026-11-23，项目引入开发与生产发布分支，并为 Cloud 作业增加了生产分支和启用开关两个条件。[项目变更 bff651a](https://github.com/shaominhyu/full-stack-starter/commit/bff651ad6470f157ec68f4e0e0475c0077fc0e63)

上述判断由工作流、手册和提交历史核实。核查一次具体发布时，还需查看实际运行的提交、仓库变量状态和结果。触发事件或作业条件变化后，复查相应步骤。

## 核对来源

- [当前 Cloud 发布工作流](../../.github/workflows/deploy.yml) <!-- sha256:2e927dd8939c8194c325d72e76723661d5fdb0ce6d80c1ae969bc41cbb3e6fc8 -->
- [当前 Cloud 部署手册](../../deployment.md#configure-continuous-deployment) <!-- sha256:aa7c420eafb7eaabebb218dd7e106cf305a402a8cefaca9e830fd95278e42198 -->
