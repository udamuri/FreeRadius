from app import app, response, config
connection = config.mysql()

def index():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `employee`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return response.ok(result, "Employee")
    except Exception as e:
        return response.badRequest(e, "Bad Request")
        
def welcome():
    return response.ok([], "Freeradius api v1.0")