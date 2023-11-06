from app import app
from app.controller import EmployeeController
from app.controller import PlanController

@app.route('/')
@app.route('/index')
def index():
    return EmployeeController.welcome()

@app.route('/plan/index', methods=['GET'])
def plan_index():
    return PlanController.index()

@app.route('/plan/store', methods=['POST'])
def plan_store():
    return PlanController.store()