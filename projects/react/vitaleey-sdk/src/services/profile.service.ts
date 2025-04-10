import { Profile } from '@/types/models/profile';
import { Request } from '@/utils/request';
import { BaseService } from './base.service';

/**
 * Profule service class for API requests
 */
export class ProfileService extends BaseService {

  /**
   * Retrieves user profile
   */
  async retrieveProfile(id: string) {
    const request = new Request(this.apiURL);
    return request.fetch<Profile>({
      url: this.detailURL(id),
      method: 'GET',
    });
  }

  /**
   * Updates user profile
   */
  async updateProfile(id: string, data: Profile) {
    const request = new Request(this.apiURL);
    return request.fetch<Profile>({
      url: this.detailURL(id),
      method: 'PATCH',
      data,
    });
  }
}

export default new ProfileService('profile');
