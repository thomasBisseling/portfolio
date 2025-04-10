import { ID } from '@/types/common';

/**
 * Ingredient model
 */
export type Ingredient = {
  id?: ID;
  name?: string;
  description?: string;
  image?: string;
  weight?: number;
  kcal?: number;
  recipeId?: ID;
};