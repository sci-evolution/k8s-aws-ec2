import type { Task } from '../types/Task';
import type { ICreateTask, IGetAllTasks, IGetTaskById, IUpdateTask, IDeleteTask } from '../interfaces/TaskInterfaces';

export class TaskService implements ICreateTask, IGetAllTasks, IGetTaskById, IUpdateTask, IDeleteTask {
  private baseUrl = '/api/tasks';

  async createTask(task: Omit<Task, 'task_id'>): Promise<Task> {
    try {
      const response = await fetch(this.baseUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task),
      });
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to create task');
        }
        throw new Error(data.error || 'Failed to create task');
      }
      return data.data;
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }

  async getAllTasks(): Promise<Task[]> {
    try {
      const response = await fetch(this.baseUrl);
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to fetch tasks');
        }
        throw new Error(data.error || 'Failed to fetch tasks');
      }
      return data.data;
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }

  async getTaskById(task_id: string): Promise<Task> {
    try {
      const response = await fetch(`${this.baseUrl}/${task_id}`);
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to fetch task');
        }
        throw new Error(data.error || 'Failed to fetch task');
      }
      return data.data;
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }

  async updateTask(task: Task): Promise<Task> {
    try {
      const response = await fetch(`${this.baseUrl}/${task.task_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(task),
      });
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to update task');
        }
        throw new Error(data.error || 'Failed to update task');
      }
      return data.data;
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }

  async deleteTask(task_id: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/${task_id}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to delete task');
        }
        throw new Error(data.error || 'Failed to delete task');
      }
      // No return value needed for delete
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }
}
