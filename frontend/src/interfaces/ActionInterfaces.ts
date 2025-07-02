// Generic interface for create (form data, no ID)
export interface IOnCreate<T, C = Omit<T, 'task_id'>> {
  onCreate(data: C): Promise<T>;
}

// Generic interface for list (no argument)
export interface IOnList<T> {
  onList(): Promise<T[]>;
}

// Generic interface for find by id (string ID)
export interface IOnFind<T> {
  onFind(id: string): Promise<T>;
}

// Generic interface for update (form data, includes ID)
export interface IOnUpdate<T, U = T> {
  onUpdate(data: U): Promise<T>;
}

// Generic interface for delete (form data: just ID or object with ID)
export interface IOnDelete<D = string> {
  onDelete(data: D): Promise<void>;
}

// Generic interface for search (form data: query object)
export interface IOnSearch<T, Q = { q: string }> {
  onSearch(query: Q): Promise<T[]>;
}
