import recipeService from '@/services/recipe.service';
import { ResponseError } from '@/types/common';
import { Recipe } from '@/types/models/recipe';
import { useState } from 'react';

const useCreateRecipe = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<ResponseError | null>(null);
  const [data, setData] = useState<Recipe>({});

  const createRecipe = (recipe: Recipe) => {
    setLoading(true);
    recipeService
      .createRecipe(recipe)
      .then((data) => {
        setData(data as Recipe);
      })
      .catch((e: ResponseError) => {
        setError(e);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return {
    createRecipe,
    loading,
    error,
    data,
  };
};

export default useCreateRecipe;
