import axios from 'axios';

/**
 * Base service class for API requests
 * @param apiPath string
 * @param apiURL string
 * @param userAgent string
 */
export class BaseService {
  private _apiURL?: string;
  private _apiPath: string;
  private _userAgent?: string;

  constructor(apiPath: string) {
    this._apiURL = process.env.API_URL || 'http://localhost:8040';
    this._userAgent = process.env.USER_AGENT || 'Recipe App';
    this._apiPath = apiPath;

    if (!this._apiURL) {
      throw new Error('API URL is required');
    }

    if (!this._userAgent) {
      throw new Error('User agent is required');
    }

    axios.defaults.baseURL = `${this._apiURL}/${this._apiPath}`;
    axios.defaults.headers.common['User-Agent'] = this._userAgent;
  }

  /**
   * Fetches all items from the API
   * @returns Promise<T[]>
   */
  protected detailURL(id: string | number): string {
    return `/${id}`;
  }

  protected get apiURL(): string {
    return this._apiURL || '';
  }
}
