import useUpdateRecipe from '@/hooks/recipe/useUpdateRecipe';
import recipeService from '@/services/recipe.service';
import { act, renderHook, waitFor } from '@testing-library/react';

describe('updateRecipe', () => {
  it('should return an updated recipe', async () => {
    const mockRecipe = {
      id: '1',
      name: 'Test Recipe',
    };

    jest.spyOn(recipeService, 'updateRecipe').mockResolvedValueOnce(mockRecipe);

    const { result } = renderHook(() => useUpdateRecipe());
    let { updateRecipe, data } = result.current;

    const recipe = { name: 'Test Recipe' };

    act(() => {
      updateRecipe(mockRecipe.id.toString(), recipe);
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

    jest.spyOn(recipeService, 'updateRecipe').mockRejectedValueOnce(mockError);

    const { result } = renderHook(() => useUpdateRecipe());
    let { updateRecipe, error } = result.current;

    const recipe = { name: 'Test Recipe' };

    act(() => {
      updateRecipe('7', recipe);
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toEqual(mockError);
    });
  });
});
