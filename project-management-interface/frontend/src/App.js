import React, { useState, useEffect } from 'react';
import ProjectForm from './components/ProjectForm';
import ProjectList from './components/ProjectList';

function App() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    const response = await fetch('http://localhost:5000/projects');
    const data = await response.json();
    setProjects(data);
  };

  const addProject = async (project) => {
    const response = await fetch('http://localhost:5000/projects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project)
    });
    const newProject = await response.json();
    setProjects([...projects, newProject]);
  };

  const deleteProject = async (projectId) => {
    await fetch(`http://localhost:5000/projects/${projectId}`, {
      method: 'DELETE'
    });
    setProjects(projects.filter(p => p.id !== projectId));
  };

  return (
    <div className="App">
      <h1>Project Management</h1>
      <ProjectForm onAddProject={addProject} />
      <ProjectList 
        projects={projects} 
        onDeleteProject={deleteProject} 
      />
    </div>
  );
}

export default App;