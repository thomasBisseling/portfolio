import recipeService from '@/services/recipe.service';
import { ResponseError } from '@/types/common';
import { useState } from 'react';

const useDeleteRecipe = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ResponseError | null>(null);
  const [data, setData] = useState<null>(null);

  const deleteRecipe = (id: string) => {
    setLoading(true);
    recipeService
      .deleteRecipe(id)
      .then(() => {
        setData(null);
      })
      .catch((e: ResponseError) => {
        setError(e);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return {
    deleteRecipe,
    loading,
    error,
    data,
  };
};

export default useDeleteRecipe;
