"use server";

import type { Task } from '../types/Task';
import type { ICreate, IGetAll, IGetById, IUpdate, IDelete, ISearch } from '../interfaces/ServiceInterfaces';

export class TaskService implements ICreate<Task>, IGetAll<Task>, IGetById<Task>, IUpdate<Task>, IDelete, ISearch<Task> {
  private baseUrl = '/api/tasks';

  async create(task: Task): Promise<Task> {
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

  async getAll(): Promise<Task[]> {
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

  async getById(task_id: string): Promise<Task> {
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

  async update(task: Task): Promise<Task> {
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

  async delete(task_id: string): Promise<void> {
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

  async search(query: { q: string }): Promise<Task[]> {
    try {
      const url = `${this.baseUrl}?search=${encodeURIComponent(query.q)}`;
      const response = await fetch(url);
      const data = await response.json();
      if (!response.ok) {
        if (process.env.NODE_ENV !== 'production') {
          console.error(data.error || 'Failed to search tasks');
        }
        throw new Error(data.error || 'Failed to search tasks');
      }
      return data.data;
    } catch (err) {
      if (process.env.NODE_ENV !== 'production') {
        console.error(err);
      }
      throw new Error((err as Error).message || 'Network error');
    }
  }
}
