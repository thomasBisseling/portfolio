import useListRecipe from '@/hooks/recipe/useListRecipe';
import recipeService from '@/services/recipe.service';
import { act, renderHook, waitFor } from '@testing-library/react';

describe('useListRecipe', () => {
  it('should return page with recipes', async () => {
    const mockRecipe = {
      results: [
        {
          id: 1,
          name: 'Test Recipe',
        },
      ],
      total: 1,
      page: 1,
      limit: 10,
    };

    jest.spyOn(recipeService, 'getRecipes').mockResolvedValueOnce(mockRecipe);

    const { result } = renderHook(() => useListRecipe());
    let { fetchRecipes, data } = result.current;

    act(() => {
      fetchRecipes();
    });

    await waitFor(() => {
      ({ data } = result.current);
      expect(data).toEqual(mockRecipe);
    });
  });

  it("should return an error when recipes can't be fetched", async () => {
    const mockError = {
      errorCode: 'ERR_5',
    };

    jest.spyOn(recipeService, 'getRecipes').mockRejectedValueOnce(mockError);

    const { result } = renderHook(() => useListRecipe());
    let { fetchRecipes, error } = result.current;

    act(() => {
      fetchRecipes();
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toEqual(mockError);
    });
  });
});
