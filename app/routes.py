from app import app
from app.controller import EmployeeController

@app.route('/')
@app.route('/index')
def index():
    return EmployeeController.welcome()