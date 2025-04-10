import { jwtDecode, JwtPayload } from 'jwt-decode';

/**
 * JWTStorage class to handle the storage of the JWT token
 * - Uses localStorage if in React Web
 * - Uses AsyncStorage if in React Native
 */
class JWTStorage {
  private _storage: Storage;
  private _tokenKey: string;

  constructor(tokenKey: string) {
    this._tokenKey = tokenKey;
    this._storage = localStorage;
  }

  // private isReactNative() {
  //   return typeof navigator != 'undefined' && navigator.product == 'ReactNative';
  // }

  set value(value: string) {
    this._storage.setItem(this._tokenKey, value);
  }

  get value() {
    return this._storage.getItem(this._tokenKey) || '';
  }

  removeValue() {
    this._storage.removeItem(this._tokenKey);
  }
}

/**
 * JWTToken class to handle a JWT token
 */
class JWTToken {
  private _value: string;
  private _storage: JWTStorage;

  constructor(tokenKey: string) {
    this._storage = new JWTStorage(tokenKey);
    this._value = '';
  }

  /**
   * Sets the value
   * @param value string
   */
  set value(value: string) {
    if (this._storage.value !== value) {
      this._storage.value = value;
    }

    this._value = this._storage.value;
  }

  /**
   * Retrieves the value
   */
  get value() {
    return this._value;
  }

  /**
   * Removes the value
   */
  removeValue() {
    this._value = '';
    this._storage.removeValue();
  }

  /**
   * Checks if the token is valid
   *
   * @param token string The token to check
   */
  isValid() {
    if (!this.value) {
      return false;
    }

    try {
      const decodedToken: JwtPayload = jwtDecode(this.value);
      if (!decodedToken.exp) {
        return false;
      }

      const expirationDate = new Date(decodedToken.exp * 1000); // Convert to milliseconds
      return expirationDate > new Date();
    } catch (error) {
      return false;
    }
  }
}

export class JWTSecurity {
  private _accessToken: JWTToken;
  private _refreshToken: JWTToken;

  constructor() {
    this._accessToken = new JWTToken('accessToken');
    this._refreshToken = new JWTToken('refreshToken');
  }

  get accessToken(): JWTToken {
    return this._accessToken;
  }

  get refreshToken(): JWTToken {
    return this._refreshToken;
  }
}

export default new JWTSecurity();
