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
    error_messages = form_validate(request)

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
                        cursor.lastrowid
                        insert_id = connection.insert_id()
                        connection.commit()
                        return response.ok(True, createRadiusPlan(insert_id), "Create Plan")
                else:
                    return response.ok(False, request.json, "Plan Already Exists")
        except Exception as e:
            return response.badRequest(e, "Bad Request")

def update(id):
    name = request.json.get("name")
    max_devices = request.json.get("max_devices")
    download = request.json.get("download")
    upload = request.json.get("upload")
    error_messages = form_validate(request)
    if len(error_messages) > 0:
        return response.ok(False, error_messages, "An Input Error Occurred")
    else:
        try:
            with connection.cursor() as cursor:
                check = "SELECT * FROM `plans` WHERE id = %s"
                cursor.execute(check, (id))
                result = cursor.fetchone()
                connection.commit()
                if result:
                    update = "UPDATE `plans` SET max_devices = %s, download = %s, upload = %s  WHERE id = %s"
                    cursor.execute(update, (max_devices, download, upload, id))
                    return createRadiusPlan(id)
                else:
                    return response.ok(False, result, f"Plan id:{id} Not found")
        except Exception as e:
            return response.badRequest(e, "Bad Request")

def createRadiusPlan(insert_id):
    try:
        with connection.cursor() as cursor:
            check = "SELECT * FROM `plans` WHERE id = %s LIMIT 1"
            cursor.execute(check, (insert_id))
            result = cursor.fetchone()
            connection.commit()
            return radiusInsert(result)
    except Exception as e:
        return response.badRequest(e, "Bad Request")
    
def radiusInsert(result):
    try:
        with connection.cursor() as cursor:
            download = result['download']
            upload = result['upload']
            delete_radgroupcheck = "DELETE FROM `radgroupcheck` WHERE groupname = %s"
            cursor.execute(delete_radgroupcheck, (result['name']))
            insert_radgroupcheck = "INSERT INTO `radgroupcheck` (groupname, attribute, op, value) VALUES (%s, %s, %s, %s)"
            val_radgroupcheck = (result['name'], 'Simultaneous-Use', ':=', result['max_devices'])
            cursor.execute(insert_radgroupcheck, val_radgroupcheck)

            delete_radgroupreply = "DELETE FROM `radgroupreply` WHERE groupname = %s"
            cursor.execute(delete_radgroupreply, (result['name']))
            insert_radgroupreply = "INSERT INTO `radgroupreply` (groupname, attribute, op, value) VALUES (%s, %s, %s, %s)"
            val_radgroupreply = (result['name'], 'Mikrotik-Rate-Limit', ':=', f"{download}M/{upload}M")
            cursor.execute(insert_radgroupreply, val_radgroupreply)

            connection.commit()
            return result
    except Exception as e:
        return response.badRequest(e, "Bad Request")
    
def form_validate(re):
    name = re.json.get("name")
    max_devices = re.json.get("max_devices")
    download = re.json.get("download")
    upload = re.json.get("upload")

    error_messages = {}
    if not name or len(name) > 100:
        error_messages['name'] = 'Name is required, or len max 100'
    if not max_devices or not type(max_devices) == int or max_devices < 1:
        error_messages['max_devices'] = 'Max devices must be a number and minimum 1'
    if not download or not type(download) == int or download < 1:
        error_messages['download'] = 'Download must be a number and minimum 1'
    if not upload or not type(upload) == int or upload < 1:
        error_messages['upload'] = 'Upload must be a number and minimum 1'

    return error_messages