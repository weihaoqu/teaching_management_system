from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DATA_FILE = 'attendance_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'classes': [], 'students': {}, 'attendance': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classes', methods=['GET', 'POST'])
def manage_classes():
    data = load_data()
    
    if request.method == 'POST':
        class_info = request.json
        class_id = f"{class_info['course_code']}_{class_info['semester']}"
        class_info['id'] = class_id
        class_info['created_at'] = datetime.now().isoformat()
        
        # Check if class already exists
        existing = next((c for c in data['classes'] if c['id'] == class_id), None)
        if existing:
            data['classes'] = [c if c['id'] != class_id else class_info for c in data['classes']]
        else:
            data['classes'].append(class_info)
            data['students'][class_id] = []
            data['attendance'][class_id] = {}
        
        save_data(data)
        return jsonify({'success': True, 'class': class_info})
    
    return jsonify(data['classes'])

@app.route('/api/classes/<class_id>', methods=['DELETE'])
def delete_class(class_id):
    data = load_data()
    data['classes'] = [c for c in data['classes'] if c['id'] != class_id]
    if class_id in data['students']:
        del data['students'][class_id]
    if class_id in data['attendance']:
        del data['attendance'][class_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/classes/<class_id>/students', methods=['GET', 'POST'])
def manage_students(class_id):
    data = load_data()
    
    if request.method == 'POST':
        student = request.json
        student['id'] = f"student_{len(data['students'].get(class_id, []))}"
        
        if class_id not in data['students']:
            data['students'][class_id] = []
        
        data['students'][class_id].append(student)
        save_data(data)
        return jsonify({'success': True, 'student': student})
    
    return jsonify(data['students'].get(class_id, []))

@app.route('/api/classes/<class_id>/students/<student_id>', methods=['PUT', 'DELETE'])
def update_student(class_id, student_id):
    data = load_data()
    
    if request.method == 'DELETE':
        if class_id in data['students']:
            data['students'][class_id] = [s for s in data['students'][class_id] if s['id'] != student_id]
        save_data(data)
        return jsonify({'success': True})
    
    if request.method == 'PUT':
        updated_student = request.json
        if class_id in data['students']:
            data['students'][class_id] = [
                updated_student if s['id'] == student_id else s 
                for s in data['students'][class_id]
            ]
        save_data(data)
        return jsonify({'success': True, 'student': updated_student})

@app.route('/api/classes/<class_id>/attendance', methods=['GET', 'POST'])
def manage_attendance(class_id):
    data = load_data()
    
    if request.method == 'POST':
        attendance_record = request.json
        date = attendance_record['date']
        
        if class_id not in data['attendance']:
            data['attendance'][class_id] = {}
        
        data['attendance'][class_id][date] = attendance_record['records']
        save_data(data)
        return jsonify({'success': True})
    
    return jsonify(data['attendance'].get(class_id, {}))

@app.route('/api/classes/<class_id>/stats')
def get_stats(class_id):
    data = load_data()
    students = data['students'].get(class_id, [])
    attendance = data['attendance'].get(class_id, {})
    
    stats = []
    for student in students:
        present = 0
        absent = 0
        late = 0
        total = len(attendance)
        
        for date, records in attendance.items():
            record = next((r for r in records if r['student_id'] == student['id']), None)
            if record:
                if record['status'] == 'present':
                    present += 1
                elif record['status'] == 'absent':
                    absent += 1
                elif record['status'] == 'late':
                    late += 1
        
        attendance_rate = (present + late) / total * 100 if total > 0 else 0
        
        stats.append({
            'student': student,
            'present': present,
            'absent': absent,
            'late': late,
            'total_sessions': total,
            'attendance_rate': round(attendance_rate, 1)
        })
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)