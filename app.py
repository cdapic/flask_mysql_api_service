from flask import Flask, request, jsonify
import pymysql
import logging
from logging.handlers import RotatingFileHandler
import os
import time

app = Flask(__name__)

# -----------------------------
# 日志系统配置
# -----------------------------

# 清理默认日志 handler，防止控制台重复输出
for handler in app.logger.handlers[:]:
    app.logger.removeHandler(handler)

# 日志目录路径
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 日志文件路径
log_path = os.path.join(log_dir, 'access.log')

# 创建一个可轮转的日志文件处理器
log_handler = RotatingFileHandler(
    log_path, maxBytes=100000, backupCount=5, encoding='utf-8'
)
log_handler.setLevel(logging.INFO)

# 日志格式：时间 - 消息
log_format = logging.Formatter('%(asctime)s - %(message)s')
log_handler.setFormatter(log_format)

# 把日志处理器绑定到 Flask 自带的 logger 上
app.logger.setLevel(logging.INFO)
app.logger.addHandler(log_handler)

# -----------------------------
# 请求开始时记录开始时间
# -----------------------------
@app.before_request
def start_timer():
    request.start_time = time.time()

# -----------------------------
# 请求结束后记录日志 + 耗时
# -----------------------------
@app.after_request
def log_request_and_response_time(response):
    try:
        duration = time.time() - request.start_time
    except AttributeError:
        duration = -1

    client_ip = request.remote_addr
    method = request.method
    path = request.path
    body = request.get_data(as_text=True)

    # 格式化日志内容
    log_msg = f"{client_ip} - {method} {path} - Body: {body} - Took {duration:.3f}s"

    # 打印到控制台 + 写入日志文件
    app.logger.info(log_msg)
    print(log_msg)

    return response

# -----------------------------
# 健康检查接口（用于浏览器验证服务是否启动）
# -----------------------------
@app.route('/')
def hello():
    return 'Hello, Flask is running!'

# -----------------------------
# MySQL 数据库连接配置
# 替换成你自己的数据库信息
# -----------------------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'chenda1993',
    'database': 'sales_db',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor  # 查询结果为 dict，便于转 JSON
}

# -----------------------------
# 执行 SQL 的接口：/execute
# 接收 JSON 请求体，字段为 "sql"
# -----------------------------
@app.route('/execute', methods=['POST'])
def execute_sql():
    try:
        sql = request.json.get('sql')
        if not sql:
            return jsonify({'error': 'Missing SQL'}), 400

        # 连接数据库并执行 SQL
        connection = pymysql.connect(**db_config)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith('select'):
                    # 查询类语句，返回结果
                    result = cursor.fetchall()
                else:
                    # 写入类语句，返回影响行数
                    connection.commit()
                    result = {'affected_rows': cursor.rowcount}

        return jsonify({'success': True, 'data': result})
    except Exception as e:
        # 异常时返回错误信息
        return jsonify({'success': False, 'error': str(e), 'code': 500}), 500

# -----------------------------
# 启动服务
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
