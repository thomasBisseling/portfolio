export type ID = string | number;

export interface Pagination<T> {
  total?: number;
  page?: number;
  limit?: number;
  results?: T[];
}

export type ResponseError = {
  error: {
    message: string;
    code: string;
  };
};
