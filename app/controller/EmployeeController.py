from app import app, response
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import pymysql.cursors
connection = pymysql.connect(host=str(os.environ.get("DB_HOST")),
                             user=str(os.environ.get("DB_USERNAME")),
                             password=str(os.environ.get("DB_PASSWORD")),
                             db=str(os.environ.get("DB_DATABASE")),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def index():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `employee`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return response.ok(result, "Hello World")
    except Exception as e:
        return response.badRequest(e, "Bad Request")