import recipeService from '@/services/recipe.service';
import { ResponseError } from '@/types/common';
import { Recipe } from '@/types/models/recipe';
import { useState } from 'react';

const useUpdateRecipe = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ResponseError | null>(null);
  const [data, setData] = useState<Recipe>({});

  const updateRecipe = (id: string, recipe: Recipe) => {
    setLoading(true);
    recipeService
      .updateRecipe(id, recipe)
      .then((data) => {
        setData(data as Recipe);
      })
      .catch((error: ResponseError) => {
        setError(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return {
    updateRecipe,
    loading,
    error,
    data,
  };
};

export default useUpdateRecipe;
