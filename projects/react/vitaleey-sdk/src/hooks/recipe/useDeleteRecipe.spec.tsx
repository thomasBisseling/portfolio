import useDeleteRecipe from '@/hooks/recipe/useDeleteRecipe';
import recipeService from '@/services/recipe.service';
import { act, renderHook, waitFor } from '@testing-library/react';

describe('useDeleteRecipe', () => {
  it('should return null when deleted recipe', async () => {
    jest.spyOn(recipeService, 'deleteRecipe').mockResolvedValueOnce({});

    const { result } = renderHook(() => useDeleteRecipe());
    let { deleteRecipe, error } = result.current;

    act(() => {
      deleteRecipe('1');
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toBeNull();
    });
  });
});
