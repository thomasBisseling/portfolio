import { User } from '@/types/models/user';
import { Request } from '@/utils/request';
import { BaseService } from './base.service';
import { Token } from '@/types/models/user';

/**
 * Auth service class for API requests
 */
export class AuthService extends BaseService {
  /**
   * Logs in a user
   * @param email string
   * @param password string
   * @returns Promise<{ token: string }>
   */
  async login(email: string, password: string) {
    const request = new Request(this.apiURL);
    return request.fetch<Token>({
      url: '/login',
      method: 'POST',
      data: { email, password },
    });
  }

  /**
   * Registers a new user
   * @param email string
   * @param password string
   * @returns Promise<User>
   */
  async register(email: string, password: string) {
    const request = new Request(this.apiURL);
    return request.fetch<void>({
      url: '/register',
      method: 'POST',
      data: { email, password },
    });
  }

  /**
   * Retrieves the current user
   * @returns Promise<{ user: { email: string } }>
   */
  async currentUser() {
    const request = new Request(this.apiURL);
    return request.fetchWithAuth<User>({
      url: '/me',
      method: 'GET',
    });
  }
}

export default new AuthService('auth');
