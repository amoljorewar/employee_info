from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'

# Create the database tables (if they don't exist already)
with app.app_context():
    db.create_all()

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# API Route to add an employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    # Validate input
    if not data or not all(key in data for key in ('name', 'position', 'salary')):
        return jsonify({"error": "Missing fields"}), 400

    # Create new employee record
    new_employee = Employee(
        name=data['name'],
        position=data['position'],
        salary=data['salary']
    )

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee added successfully!"}), 201

# API Route to delete an employee by ID
@app.route('/delete_employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": f"Employee {id} deleted successfully!"}), 200

# API Route to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employee_list = []

    for employee in employees:
        employee_list.append({
            'id': employee.id,
            'name': employee.name,
            'position': employee.position,
            'salary': employee.salary
        })

    return jsonify(employee_list), 200

# Start the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

