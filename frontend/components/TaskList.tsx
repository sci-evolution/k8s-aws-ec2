import React from 'react';
import Link from 'next/link';

type Task = {
  id: string | number;
  title: string;
};

type TaskListProps = {
  tasks?: Task[];
};

const TaskList: React.FC<TaskListProps> = ({ tasks = [] }) => {
  return (
    <section>
      <h2>Tasks</h2>
      <ul style={{ padding: 0, listStyle: 'none' }}>
        {tasks.length === 0 && <li>No tasks found.</li>}
        {tasks.map(task => (
          <li key={task.id} style={{ padding: '0.5rem 0', borderBottom: '1px solid #eee' }}>
            <Link href={`/tasks/${task.id}`} style={{ textDecoration: 'none', color: '#333' }}>{task.title}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default TaskList;
