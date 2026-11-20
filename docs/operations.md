# 本地运行与部署

本地开发使用 Docker Compose 运行 PostgreSQL 18 和 Mailpit，FastAPI 和 Vite 在本机运行。开发服务通过本机回环地址访问。需要查看数据库时，可以单独启动 Adminer。

| 服务 | 默认入口 |
| --- | --- |
| 前端登录页 | [localhost:5173/login](http://localhost:5173/login) |
| API 文档 | [localhost:8000/docs](http://localhost:8000/docs) |
| API 健康检查 | [localhost:8000/api/v1/utils/health-check/](http://localhost:8000/api/v1/utils/health-check/) |
| Mailpit 测试邮箱 | [localhost:8025](http://localhost:8025) |
| PostgreSQL | `127.0.0.1:5432`，数据库名 `app` |
| Adminer（按需） | [localhost:8081](http://localhost:8081) |

## 本地启动

以下命令从仓库根目录执行，适用于 Bash。代码块共用启动容器时定义的 `root` 和 `compose` 变量。分开调用命令时，在该调用中重新定义需要的变量。启动前确认 Docker 正在运行。若项目服务已运行且验证通过，直接返回访问地址。端口被占用时，先确认进程归属。

首次安装或锁文件更新后同步依赖。Python 版本见根目录的 `.python-version`，Python 依赖用 uv，前端依赖用 Bun。已有可用依赖的日常启动可直接从启动容器开始。

```bash
uv sync --locked --no-dev --package app
bun install --frozen-lockfile
```

机器上已有 npm 时，也可以用 `npx --yes bun install --frozen-lockfile` 执行前端安装。后面的 `npm run dev` 只调用已安装的 Vite。

### 启动数据库和测试邮箱

本地覆盖文件首次启动时生成，后续沿用。Compose 项目名 `fullstack-local` 对应现有数据库卷 `fullstack-local_app-db-data`。

```bash
root="$(git rev-parse --show-toplevel)"
cd "$root" || exit
local_dir="$(git rev-parse --absolute-git-dir)/local-runtime"
mkdir -p "$local_dir"
if [[ ! -f "$local_dir/compose.loopback.yml" ]]; then
  cat > "$local_dir/compose.loopback.yml" <<'YAML'
services:
  db:
    image: postgres:18-alpine
    ports: !override
      - "127.0.0.1:5432:5432"
  mailpit:
    ports: !override
      - "127.0.0.1:8025:8025"
      - "127.0.0.1:1025:1025"
  adminer:
    ports: !override
      - "127.0.0.1:8081:8080"
    environment:
      ADMINER_DEFAULT_SERVER: db
YAML
fi
compose=(docker compose -p fullstack-local -f compose.yml -f compose.override.yml
  -f "$local_dir/compose.loopback.yml")
"${compose[@]}" up -d --wait db mailpit
```

### 准备数据库

第一次启动或拉取了新的数据库迁移时执行。脚本先将本地库迁移到最新版本，再在需要时创建首个管理员。迁移前确认实际使用的 `DATABASE_URL` 指向本机开发库。开发账号取自根目录 `.env` 的 `FIRST_SUPERUSER` 和 `FIRST_SUPERUSER_PASSWORD`。

```bash
(
  cd "$root/backend" || exit
  PATH="$root/.venv/bin:$PATH" bash scripts/prestart.sh
)
```

### 启动应用

在 Linux 用户会话中用下面的命令让前后端在后台运行。已有的活动服务会被复用。机器重启后按本节重新启动。若当前环境没有 systemd 用户会话，在两个终端分别进入命令指定的目录，直接运行对应的 FastAPI 和 Vite 命令。

```bash
if ! systemctl --user is-active --quiet fullstack-local-api; then
  systemd-run --user --unit=fullstack-local-api --collect \
    --working-directory="$root/backend" \
    --setenv="PATH=$root/.venv/bin:$PATH" \
    "$root/.venv/bin/fastapi" dev --host 127.0.0.1 --port 8000
fi
if ! systemctl --user is-active --quiet fullstack-local-web; then
  systemd-run --user --unit=fullstack-local-web --collect \
    --working-directory="$root/frontend" --setenv="PATH=$PATH" \
    "$(command -v npm)" run dev -- --host 127.0.0.1 --port 5173 --strictPort
fi
```

### 验证和停止

前端登录页应返回 HTTP 200，API 健康检查应返回 `true`，Mailpit 页面应可访问。健康检查只确认 API 可以响应。需要验证整条链路时，在浏览器登录并创建一条临时记录，刷新确认可见，然后清理该记录。

```bash
curl -fsS --retry 10 --retry-connrefused --retry-delay 1 -o /dev/null http://localhost:5173/login
curl -fsS --retry 10 --retry-connrefused --retry-delay 1 http://localhost:8000/api/v1/utils/health-check/
curl -fsS --retry 10 --retry-connrefused --retry-delay 1 -o /dev/null http://localhost:8025/
"${compose[@]}" ps db mailpit
```

应用失败时用 `journalctl --user -u fullstack-local-api -u fullstack-local-web -n 100` 查看日志。数据库和邮件服务日志用 `"${compose[@]}" logs --tail 100 db mailpit` 查看。

停止后台应用后，可以用 Compose 的 `stop` 停止开发容器并保留数据库卷。后续用相同的项目名和配置启动即可继续使用这些数据。

```bash
systemctl --user stop fullstack-local-web fullstack-local-api
"${compose[@]}" stop db mailpit adminer
```

## 查看和操作本地数据库

Adminer 是模板自带的图形化数据库管理工具。已有本地覆盖文件时，确认它包含上面配置里的 `adminer` 段，端口绑定在 `127.0.0.1`。使用同一组 Compose 参数启动，Adminer 会连接现有的开发数据库。

```bash
"${compose[@]}" up -d --wait db adminer
```

打开 [Adminer](http://localhost:8081)，选择 PostgreSQL，服务器填 `db`，用户名填 `postgres`，数据库填 `app`。密码取自根目录 `.env` 的 `POSTGRES_PASSWORD`。可以用「选择数据」筛选、查看记录，也可以在「SQL 命令」里运行查询。

如果想直接使用 PostgreSQL 命令行，在仓库根目录执行：

```bash
"${compose[@]}" exec db psql -U postgres -d app
```

## 生产部署和 CI/CD

生产设置和发布命令以对应的上游文档为准。生产数据库和密钥由部署环境提供。

| 任务 | 入口 |
| --- | --- |
| 自托管部署 | [Docker Compose 部署说明](../deployment-docker-compose.md)。使用 `compose.yml` 与 `compose.deploy.yml`，Traefik 提供 HTTPS，发布工作流由服务器上的自托管 Runner 手动触发。 |
| FastAPI Cloud 部署 | [FastAPI Cloud 部署说明](../deployment.md)。配置外部 PostgreSQL 和部署凭据后，在 GitHub Actions 手动运行 `Deploy`。 |
| GitHub Actions | [工作流目录](../.github/workflows/)，包含 API 测试、Playwright、Compose 启动检查和两条发布路径。 |
| 上游本地开发方式 | [开发说明](../development.md)，包括全容器运行、邮件和配置。 |
