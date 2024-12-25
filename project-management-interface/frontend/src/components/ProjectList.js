import React from 'react';

function ProjectList({ projects, onDeleteProject }) {
  return (
    <div>
      <h2>Projects</h2>
      {projects.map(project => (
        <div key={project.id}>
          <h3>{project.name}</h3>
          <p>Repository: {project.repository}</p>
          <p>{project.description}</p>
          <button onClick={() => onDeleteProject(project.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default ProjectList;