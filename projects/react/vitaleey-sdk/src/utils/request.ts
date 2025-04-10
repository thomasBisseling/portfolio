import jwtSecurity from '@/security/jwt.security';
import { ResponseError } from '@/types/common';
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

export type Response<T> = T | ResponseError;

type Token = {
  token?: string;
};

export class Request {
  private _request: AxiosInstance;

  constructor(apiURL: string, headers?: { [key: string]: string }) {
    if (!apiURL) {
      throw new Error('API URL is required');
    }

    this._request = axios.create({
      baseURL: apiURL,
      headers: headers,
    });
  }

  public getNewToken() {
    if (!jwtSecurity.refreshToken.value) {
      return '';
    }

    const request = new Request('token');
    request
      .fetch<Token>({
        url: '/refresh',
        method: 'POST',
        data: { refreshToken: jwtSecurity.refreshToken.value },
      })
      .then((data) => {
        data = data as Token;
        if (data && data.token) {
          jwtSecurity.accessToken.value = data.token;
        }
      })
      .catch(() => {
        jwtSecurity.accessToken.removeValue();
      });

    return jwtSecurity.accessToken.value;
  }

  private isResponseError(statusCode: any) {
    return statusCode > 399 && statusCode < 600;
  }

  private readableResponse<T>(resp: AxiosResponse<any, any>): T | ResponseError {
    if (this.isResponseError(resp.status)) {
      return {
        error: {
          message: resp.data.toString(),
          code: resp.data.toString(),
        },
      };
    } else {
      return {
        ...resp.data,
      };
    }
  }

  /**
   * Make request to the API
   * @param options AxiosRequestConfig
   * @returns Promise<T | ResponseError>
   */
  async fetch<T>(options: AxiosRequestConfig): Promise<Response<T>> {
    const response = await this._request({ ...options });
    const readableResponse = this.readableResponse<T>(response);

    if (this.isResponseError(response.status)) {
      return Promise.reject(readableResponse);
    }

    return readableResponse;
  }

  /**
   * Make request to the API with authentication
   * @param options AxiosRequestConfig
   * @returns Promise<T | ResponseError>
   */
  async fetchWithAuth<T>(options: AxiosRequestConfig): Promise<Response<T>> {
    const instance = axios.create();
    instance.defaults.baseURL = this._request.defaults.baseURL;
    instance.defaults.headers = this._request.defaults.headers;
    instance.interceptors.request.use(
      (config) => {
        const accessToken = jwtSecurity.accessToken;
        if (accessToken.value) {
          config.headers.Authorization = `Bearer ${jwtSecurity}`;
          if (!accessToken.isValid()) {
            const newToken = this.getNewToken();
            if (newToken) {
              config.headers.Authorization = `Bearer ${newToken}`;
            }
          }
        }

        return config;
      },
      (error) => {
        return Promise.reject(error);
      },
    );

    const response = await instance.request({ ...options });
    const readableResponse = this.readableResponse<T>(response);

    if (this.isResponseError(response.status)) {
      return Promise.reject(readableResponse);
    }

    return readableResponse;
  }
}
