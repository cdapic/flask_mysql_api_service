# Flask SQL Execution Service

## Introduction

This is a Flask-based Web service used to execute SQL statements and return the results. The service has a logging function that can record detailed information about each request and its processing time.

## Features

- **Health check interface `/`**: Used to verify if the service is successfully started.
- **SQL execution interface `/execute`**: Receives a JSON-formatted request body containing the `sql` field, executes the corresponding SQL statement, and returns the result.

## Install Dependencies

Execute the following command in the project root directory to install the required Python dependencies:

  

bash

```bash
pip install -r requirements.txt
```

## Configure the Database

Find the `db_config` dictionary in the `app.py` file and replace it with your own database information:

  

python

运行

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'sales_db',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor  # Query results are in dict format for easy conversion to JSON
}
```

## Start the Service

Execute the following command in the project root directory to start the service:

  

bash

```bash
python app.py
```

## Usage

### Health Check

Access `http://localhost:5000` in your browser. If it displays `Hello, Flask is running!`, it means the service has been successfully started.

### Execute SQL

Use a tool (such as Postman) to send a POST request to `http://localhost:5000/execute`. The request body should be in JSON format and contain the `sql` field, as shown in the following example:

  

json

```json
{
    "sql": "SELECT * FROM your_table"
}
```

  

## Logs

The service will record detailed information about each request (including client IP, request method, request path, request body, and processing time) in the `logs/access.log` file.

## Attention

Currently, this service is only suitable as an internal network MVP interface!!