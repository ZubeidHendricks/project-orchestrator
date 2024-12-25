from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Project, db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db.init_app(app)

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    new_project = Project(
        name=data['name'],
        repository=data['repository'],
        description=data.get('description', '')
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)