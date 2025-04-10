import { AuthService } from '@/services/auth.service';
import { Pagination } from '@/types/common';
import { Ingredient } from '@/types/models/ingredient';
import { Recipe } from '@/types/models/recipe';
import { Request } from '@/utils/request';

export class RecipeService extends AuthService {
  /**
   * Fetches all recipes from the API
   * @returns Promise<Recipe[]>
   */
  async getRecipes() {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Pagination<Recipe>>({ method: 'GET' });
  }

  /**
   * Fetches all ingredients of recipe from the API
   * @returns Promise<Recipe[]>
   */
  async fetchRecipesIngredients(id: string) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Ingredient[]>({ url: `recipes/${id}/ingredients`, method: 'GET' });
  }

  /**
   * Fetches all ingredients of recipe from the API
   * @returns Promise<Recipe[]>
   */
  async assignIngredientToRecipe(id: string, ingredientId: string) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Recipe>({
      url: `recipes/${id}/ingredients/${ingredientId}`,
      method: 'POST',
    });
  }

  /**
   * Fetches a single recipe from the API
   * @param id string
   * @returns Promise<Recipe>
   */
  async getRecipe(id: string | number) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Recipe>({ url: this.detailURL(id), method: 'GET' });
  }

  /**
   * Creates a new recipe
   * @param recipe Recipe
   * @returns Promise<Recipe>
   */
  async createRecipe(recipe: Recipe) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Recipe>({
      method: 'POST',
      data: recipe,
    });
  }

  /**
   * Updates a recipe with the given ID
   * @param id string
   * @param recipe Recipe
   * @returns Promise<Recipe>
   */
  async updateRecipe(id: string, recipe: Recipe) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Recipe>({
      url: this.detailURL(id),
      method: 'PUT',
      data: recipe,
    });
  }

  /**
   * Deletes a recipe with the given ID
   * @param id string
   * @returns Promise<Recipe>
   */
  async deleteRecipe(id: string) {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<Recipe>({
      url: this.detailURL(id),
      method: 'DELETE',
    });
  }
}

export default new RecipeService('recipes');
