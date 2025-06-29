import React from 'react';

type TaskFormProps = {
  onSubmit: React.FormEventHandler<HTMLFormElement>;
  initialData?: {
    title?: string;
    description?: string;
    priority?: string;
    status?: string;
  };
};

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, initialData = {} }) => {
  return (
    <form onSubmit={onSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: 500 }}>
      <input name="title" placeholder="Title" defaultValue={initialData.title || ''} required />
      <textarea name="description" placeholder="Description" defaultValue={initialData.description || ''} />
      <select name="priority" defaultValue={initialData.priority || 'LOW'}>
        <option value="LOW">Low</option>
        <option value="MEDIUM">Medium</option>
        <option value="HIGH">High</option>
      </select>
      <select name="status" defaultValue={initialData.status || 'TODO'}>
        <option value="TODO">To Do</option>
        <option value="DOING">Doing</option>
        <option value="DONE">Done</option>
      </select>
      <button type="submit">Save Task</button>
    </form>
  );
};

export default TaskForm;
