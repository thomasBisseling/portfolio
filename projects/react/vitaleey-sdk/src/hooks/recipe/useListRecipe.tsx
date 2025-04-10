import recipeService from '@/services/recipe.service';
import { Pagination, ResponseError } from '@/types/common';
import { Recipe } from '@/types/models/recipe';
import { useState } from 'react';

const useListRecipes = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ResponseError | null>(null);
  const [data, setData] = useState<Pagination<Recipe>>({});

  const fetchRecipes = () => {
    setLoading(true);
    recipeService
      .getRecipes()
      .then((data) => {
        setData(data as Pagination<Recipe>);
      })
      .catch((e: ResponseError) => {
        setError(e);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return {
    fetchRecipes,
    loading,
    error,
    data,
  };
};

export default useListRecipes;
