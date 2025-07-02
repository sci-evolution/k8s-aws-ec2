"use server";

import { TaskService } from '../services/TaskService';
import type { Task } from '../types/Task';
import type {
  IOnCreate,
  IOnList,
  IOnFind,
  IOnUpdate,
  IOnDelete,
  IOnSearch
} from '../interfaces/ActionInterfaces';

export class TaskActions implements
  IOnCreate<Task, Omit<Task, 'task_id'>>,
  IOnList<Task>,
  IOnFind<Task>,
  IOnUpdate<Task, Task>,
  IOnDelete<string>,
  IOnSearch<Task, { q: string }> {
  private service = new TaskService();

  async onCreate(data: Omit<Task, 'task_id'>): Promise<Task> {
    return this.service.create(data as Task);
  }

  async onList(): Promise<Task[]> {
    return this.service.getAll();
  }

  async onFind(id: string): Promise<Task> {
    return this.service.getById(id);
  }

  async onUpdate(data: Task): Promise<Task> {
    return this.service.update(data);
  }

  async onDelete(id: string): Promise<void> {
    return this.service.delete(id);
  }

  async onSearch(query: { q: string }): Promise<Task[]> {
    return this.service.search(query);
  }
}
