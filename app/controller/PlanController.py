from app import app, response, config
from flask import request
connection = config.mysql()
        
def index():
    return response.ok([], "Freeradius api v1.0")

def store():
    name = request.json.get("name")
    max_devices = request.json.get("max_devices")
    download = request.json.get("download")
    upload = request.json.get("upload")

    error_messages = {}
    if not name :
        error_messages['name'] = 'Name is required'
    if not max_devices or not type(max_devices) == int or max_devices < 1:
        error_messages['max_devices'] = 'Max devices must be a number and minimum 1'
    if not download or not type(download) == int or download < 1:
        error_messages['download'] = 'Download must be a number and minimum 1'
    if not upload or not type(upload) == int or upload < 1:
        error_messages['upload'] = 'Upload must be a number and minimum 1'

    if len(error_messages) > 0:
        return response.ok(0, error_messages, "An Input Error Occurred")
    else:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `plans`"
                cursor.execute(sql)
                result = cursor.fetchall()
                return response.ok(1, result, "Create Plan")
        except Exception as e:
            return response.badRequest(e, "Bad Request")