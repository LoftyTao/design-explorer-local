# Design Explorer

一个强大的设计数据可视化和探索工具，使用 Python 和 Dash 构建。

## 功能特点

- **交互式数据可视化**：通过平行坐标图探索设计数据
- **数据点颜色编码**：根据不同参数对数据点进行颜色编码，便于识别模式
- **图像探索**：基于设计参数查看和比较图像
- **排序和过滤**：根据任何参数对图像进行排序，并使用平行坐标图过滤数据
- **示例项目**：内置示例项目，方便快速探索
- **ZIP 文件上传**：从 ZIP 文件加载自定义设计数据
- **响应式设计**：在不同屏幕尺寸上都能良好工作

## 安装

### 前提条件

- Python 3.8 或更高版本
- pip 包管理器

### 安装依赖

1. 克隆仓库：

```bash
git clone https://github.com/LoftyTao/design-explorer-local.git
cd design-explorer-local
```

2. 创建虚拟环境（可选但推荐）：

```bash
# Windows 系统
python -m venv venv
venv\Scripts\activate

# macOS/Linux 系统
python3 -m venv venv
source venv/bin/activate
```

3. 安装所需依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行应用程序

```bash
cd app
python app.py
```

应用程序将在 http://127.0.0.1:8050/ 上启动

### 使用 Design Explorer

1. **选择项目**：从内置示例项目中选择或上传自己的 ZIP 文件
2. **参数颜色编码**：使用 "Color by" 下拉菜单根据参数对数据点进行颜色编码
3. **排序图像**：使用 "Sort by" 下拉菜单根据参数对图像进行排序
4. **探索图像**：点击图像在选定图像面板中查看详情
5. **过滤数据**：通过在平行坐标图的轴上拖动来过滤数据点
6. **查看数据表**：向下滚动查看完整的数据表

## 示例项目

Design Explorer 包含多个示例项目，帮助您快速入门：

- **Daylight Factor**：探索日光模拟结果
- **Box**：3D 盒子设计变体
- **Box Without Images**：无图像的参数变体

## 创建自定义项目

要创建自己的项目，请准备一个具有以下结构的 ZIP 文件：

```
project-name/
├── data.csv          # 主数据文件
└── images/           # data.csv 中引用的图像文件
    ├── image1.png
    ├── image2.png
    └── ...
```

### 数据 CSV 格式

`data.csv` 文件应包含您的设计参数和图像引用：

```csv
param1,param2,param3,img:Image
a,b,c,image1.png
d,e,f,image2.png
...
```

- 对图像列使用 `img:` 前缀
- 使用描述性列名以提高可读性

## 技术栈

- **前端**：Dash (Plotly)、HTML、CSS、Bootstrap
- **后端**：Python、Flask
- **数据处理**：Pandas、NumPy
- **可视化**：Plotly Express

## 开发

### 项目结构

```
design-explorer/
├── app/                  # 主应用程序代码
│   ├── callbacks/        # Dash 回调函数
│   ├── containers/       # UI 组件容器
│   ├── assets/           # 静态资源（CSS、图像）
│   └── app.py            # 应用程序入口点
├── README.md             # 英文 README
├── README_CN.md          # 中文 README
└── requirements.txt      # 依赖项
```

### 添加新功能

1. 为您的功能创建一个新分支
2. 实现您的更改
3. 彻底测试
4. 提交拉取请求

### 运行测试

```bash
# 运行测试（如果可用）
pytest
```

## 贡献

欢迎贡献！请随时提交问题和拉取请求。

1. Fork 仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开拉取请求

## 许可证

本项目采用 MIT 许可证 - 详情请查看 LICENSE 文件。

## 致谢

- 使用 [Dash](https://dash.plotly.com/) 和 [Plotly](https://plotly.com/) 构建
- 灵感来自设计优化工作流
- 感谢所有贡献者

## 联系方式

如有问题或反馈，请在 GitHub 上打开 issue 或联系维护者。

---

*探索愉快！*