import React, { useState } from 'react';

function ProjectForm({ onAddProject }) {
  const [name, setName] = useState('');
  const [repository, setRepository] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddProject({ name, repository, description });
    setName('');
    setRepository('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Project Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Repository URL"
        value={repository}
        onChange={(e) => setRepository(e.target.value)}
        required
      />
      <textarea
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button type="submit">Add Project</button>
    </form>
  );
}

export default ProjectForm;