# 项目脉络

Full Stack Starter 基于 Full Stack FastAPI Template，为带身份验证、数据库和前端界面的应用提供开发与发布起点。[项目说明](../README.md)

目前收录部署和提交合并请求两个主题。接手时按任务或现象找入口，打开条目后先看适用条件和当前结论。

| 遇到的任务或现象 | 从这里开始 |
| --- | --- |
| 部署测试环境或生产环境，选择 Cloud 或自托管 Compose | [部署指南](guides/deployment.md) |
| 合并后没有 Cloud 部署，或手动发布时任务被跳过 | [Cloud 部署由什么触发](questions/cloud-deploy-trigger.md) |
| 提交任务 PR / MR 到 develop，或准备 develop → master 发布 PR | [提交合并请求](guides/merge-request.md) |

本地启动和日常操作可以直接查[运维手册](../docs/operations.md)。查规范时以适用的正式手册为依据，查历史原因时可以沿条目里的证据回溯。

## 怎么使用

- **第一次沉淀**　用户可以说「把这次排障的方法和踩过的坑记下来」，也可以只指定其中一部分。按[问题记录模板](questions/README.md)或[流程指南模板](guides/README.md)建页，并把下次可能用来找它的任务名称、症状或别名加到上表。
- **再次接手**　命中条目时，在仓库根目录运行 `python3 context/check.py`，再核对当前任务的环境和来源。遇到未收录的任务，照常使用项目文档。
- **发现变化**　按[维护约定](maintenance.md)处理，重要替换和仍待核实的冲突可在[变更记录](log.md)追溯。需随项目保留的原始材料见[来源说明](sources/README.md)。
