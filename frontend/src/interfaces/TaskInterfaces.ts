import type { Task } from '../types/Task';

// Interface for creating a task
export interface ICreateTask {
  createTask(task: Omit<Task, 'task_id'>): Promise<Task>;
}

// Interface for getting all tasks
export interface IGetAllTasks {
  getAllTasks(): Promise<Task[]>;
}

// Interface for getting a task by ID
export interface IGetTaskById {
  getTaskById(task_id: string): Promise<Task>;
}

// Interface for updating a task
export interface IUpdateTask {
  updateTask(task: Task): Promise<Task>;
}

// Interface for deleting a task
export interface IDeleteTask {
  deleteTask(task_id: string): Promise<void>;
}
