export type TaskPriority = 'HIGH' | 'MEDIUM' | 'LOW';
export type TaskStatus = 'TODO' | 'DOING' | 'DONE';

export interface Task {
  task_id: string;
  title: string;
  description?: string;
  start_time?: string | null;
  end_time?: string | null;
  priority: TaskPriority;
  status: TaskStatus;
}
