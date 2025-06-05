# Flask SQL 执行服务

## 简介

这是一个基于 Flask 的 Web 服务，用于执行 SQL 语句并返回结果。该服务具备日志记录功能，能够记录每个请求的详细信息以及处理耗时。

## 功能

- **健康检查接口 `/`**：用于验证服务是否成功启动。
- **执行 SQL 接口 `/execute`**：接收 JSON 格式的请求体，其中包含 `sql` 字段，执行相应的 SQL 语句并返回结果。

## 安装依赖

在项目根目录下执行以下命令安装所需的 Python 依赖：

  

bash

```bash
pip install -r requirements.txt
```

## 配置数据库

在 `app.py` 文件中找到 `db_config` 字典，将其替换为你自己的数据库信息：

  

python

运行

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'chenda1993',
    'database': 'sales_db',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor  # 查询结果为 dict，便于转 JSON
}
```

## 启动服务

在项目根目录下执行以下命令启动服务：

  

bash

```bash
python app.py
```

## 使用方法

### 健康检查

在浏览器中访问 `http://localhost:5000`，若显示 `Hello, Flask is running!`，则表示服务已成功启动。

### 执行 SQL

使用工具（如 Postman）发送 POST 请求到 `http://localhost:5000/execute`，请求体为 JSON 格式，包含 `sql` 字段，示例如下：

  

json

```json
{
    "sql": "SELECT * FROM your_table"
}
```

## 日志

服务会将每个请求的详细信息（包括客户端 IP、请求方法、请求路径、请求体和处理耗时）记录到 `logs/access.log` 文件中。

## 注意
目前该服务仅适合作为内网 MVP 接口！！
