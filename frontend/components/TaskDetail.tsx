import React from 'react';

type Task = {
  id: string | number;
  title: string;
  description?: string;
  priority?: string;
  status?: string;
};

type TaskDetailProps = {
  task?: Task;
};

const TaskDetail: React.FC<TaskDetailProps> = ({ task }) => {
  if (!task) return <div>Task not found.</div>;
  return (
    <section>
      <h2>{task.title}</h2>
      <p><strong>Description:</strong> {task.description}</p>
      <p><strong>Priority:</strong> {task.priority}</p>
      <p><strong>Status:</strong> {task.status}</p>
      {/* Add more task details here */}
    </section>
  );
};

export default TaskDetail;
