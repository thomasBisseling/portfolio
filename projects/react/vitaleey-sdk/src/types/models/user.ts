import { ID } from '@/types/common';

export type User = {
  id?: ID;
  email?: string;
  name?: string;
  role?: string;
};

export type Token = {
  token?: string;
  refreshToken?: string;
};
