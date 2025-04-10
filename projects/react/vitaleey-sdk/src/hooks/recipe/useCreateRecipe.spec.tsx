import recipeService from '@/services/recipe.service';
import { Recipe } from '@/types/models/recipe';
import { act, renderHook, waitFor } from '@testing-library/react';
import useCreateRecipe from './useCreateRecipe';

describe('useCreateRecipe', () => {
  it('should return a new recipe', async () => {
    const mockRecipe: Recipe = {
      id: '1',
      name: 'Test Recipe',
    };

    jest.spyOn(recipeService, 'createRecipe').mockResolvedValueOnce(mockRecipe);

    const { result } = renderHook(() => useCreateRecipe());
    let { createRecipe, data } = result.current;

    const recipe = { name: 'Test Recipe' };

    act(() => {
      createRecipe(recipe);
    });

    await waitFor(() => {
      ({ data } = result.current);
      expect(data).toEqual(mockRecipe);
    });
  });

  it('should return an error if the recipe is invalid', async () => {
    const mockError = {
      errorCode: 'ERR11',
    };

    jest.spyOn(recipeService, 'createRecipe').mockRejectedValueOnce(mockError);

    const { result } = renderHook(() => useCreateRecipe());
    let { createRecipe, error } = result.current;

    const recipe = { name: 'Test Recipe' };

    act(() => {
      createRecipe(recipe);
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toEqual(mockError);
    });
  });
});
