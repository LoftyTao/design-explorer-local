# Design Explorer (Offline Version)

这是一个经过改造的 Design Explorer 应用程序，旨在支持完全离线运行。原有的 Pollination 云集成功能已被禁用或替换为本地占位符。

## 功能变更

- **移除在线依赖**：移除了 `pollination-io` 等需要网络连接的库。
- **本地资源**：Bootstrap CSS 和其他静态资源已下载到本地 `assets` 文件夹，不再依赖 CDN。
- **移除外部 API**：移除了 Pollination API 认证和 YouTube 视频嵌入。
- **仅限样本项目**：目前仅支持加载本地样本项目（如 Daylight Factor）。

## 安装与运行

### 1. 环境准备

建议使用 Python 虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
.\venv\Scripts\activate

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate
```

### 2. 安装依赖

进入 `app` 目录并安装依赖：

```bash
cd app
pip install -r requirements.txt
```

### 3. 运行应用

在 `app` 目录下运行：

```bash
python app.py
```

应用启动后，请在浏览器中访问： http://127.0.0.1:8050/

## 目录结构说明

- `app.py`: 主应用程序入口。
- `assets/`: 包含 CSS、图片和样本数据等静态资源。
- `containers.py`: UI 组件定义（已修改为离线模式）。
- `callbacks/`: 交互逻辑回调函数。
- `download_assets.py`: 用于下载离线资源的脚本（已执行，资源已就绪）。
