from app import app, response, config
from flask import request
connection = config.mysql()
        
def index():
    return response.ok(True, [], "Freeradius api v1.0")

def store():
    name = request.json.get("name")
    max_devices = request.json.get("max_devices")
    download = request.json.get("download")
    upload = request.json.get("upload")

    error_messages = {}
    if not name or len(name) > 100:
        error_messages['name'] = 'Name is required, or len max 100'
    if not max_devices or not type(max_devices) == int or max_devices < 1:
        error_messages['max_devices'] = 'Max devices must be a number and minimum 1'
    if not download or not type(download) == int or download < 1:
        error_messages['download'] = 'Download must be a number and minimum 1'
    if not upload or not type(upload) == int or upload < 1:
        error_messages['upload'] = 'Upload must be a number and minimum 1'

    if len(error_messages) > 0:
        return response.ok(False, error_messages, "An Input Error Occurred")
    else:
        try:
            lower_name = name.lower()
            with connection.cursor() as cursor:
                check = "SELECT id FROM `plans` WHERE name = %s LIMIT 1"
                cursor.execute(check, (lower_name))
                if cursor.rowcount == 0:
                    sql = "INSERT INTO `plans` (name, max_devices, download, upload) VALUES (%s, %s, %s, %s)"
                    val = (lower_name, max_devices, download, upload)
                    if cursor.execute(sql, val):
                        connection.commit()
                        return response.ok(True, request.json, "Create Plan")
                else:
                    return response.ok(False, request.json, "Plan Already Exists")
        except Exception as e:
            return response.badRequest(e, "Bad Request")
        