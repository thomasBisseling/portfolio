import { ID } from '@/types/common';

export type Profile = {
  id?: ID;
  userId?: ID;
  name?: string;
  bio?: string;
  avatar?: string;
  location?: string;
  website?: string;
  createdAt?: string;
  updatedAt?: string;
};