from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for /api/* routes

# Load student data from JSON file
def load_student_data():
    file_path = os.path.join(os.path.dirname(__file__), '../data/students.json')
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

students = load_student_data()

@app.route('/api', methods=['GET'])
def get_marks():
    # Get names from query parameters (name=X&name=Y)
    names = request.args.getlist('name')
    if not names:
        return jsonify({"error": "At least one name is required"}), 400

    # Find marks for the provided names in order
    marks = []
    student_dict = {student['name']: student['marks'] for student in students}
    
    for name in names:
        if name in student_dict:
            marks.append(student_dict[name])
        else:
            return jsonify({"error": f"Name '{name}' not found"}), 404

    return jsonify({"marks": marks})

if __name__ == '__main__':
    app.run(debug=True)
