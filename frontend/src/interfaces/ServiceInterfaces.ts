// Interface for creating an item (generic)
export interface ICreate<T> {
  create(item: T): Promise<T>;
}

// Interface for getting all items (generic)
export interface IGetAll<T> {
  getAll(): Promise<T[]>;
}

// Interface for getting an item by ID (generic)
export interface IGetById<T> {
  getById(id: string): Promise<T>;
}

// Interface for updating an item (generic)
export interface IUpdate<T> {
  update(item: T): Promise<T>;
}

// Interface for deleting an item (generic)
export interface IDelete {
  delete(id: string): Promise<void>;
}

// Interface for searching items (generic)
export interface ISearch<T, Q = { q: string }> {
  search(query: Q): Promise<T[]>;
}
