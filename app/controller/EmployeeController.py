from app import app, response

def index():
    try:
        return response.ok([], "Hello World")
    except Exception as e:
        return e