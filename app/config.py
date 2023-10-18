from flask import jsonify, make_response
import pymysql.cursors

def mysql():
    connection = pymysql.connect(host=str("127.0.0.1"),
                             user=str("root"),
                             password=str("123456"),
                             db=str("flask_employee"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    return connection