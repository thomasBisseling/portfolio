import jwt from 'jsonwebtoken';
import { JWTSecurity } from './jwt.security';

describe('JWTSecurity', () => {
  let jwtSecurity: JWTSecurity;

  beforeEach(() => {
    jwtSecurity = new JWTSecurity();
  });

  it('should set accessToken', () => {
    const value = 'test';

    jwtSecurity.accessToken.value = value;

    expect(localStorage.getItem('accessToken')).toBe(value);
  });

  it('should get accessToken', () => {
    const value = 'test';

    jwtSecurity.accessToken.value = value;

    expect(jwtSecurity.accessToken.value).toBe(value);
  });

  it('should remove accessToken', () => {
    const value = 'test';

    jwtSecurity.accessToken.value = value;
    jwtSecurity.accessToken.removeValue();

    expect(jwtSecurity.accessToken.value).toBe('');
  });

  it('should set refreshToken', () => {
    const value = 'test';

    jwtSecurity.refreshToken.value = value;

    expect(localStorage.getItem('refreshToken')).toBe(value);
  });

  it('should get refreshToken', () => {
    const value = 'test';

    jwtSecurity.refreshToken.value = value;

    expect(jwtSecurity.refreshToken.value).toBe(value);
  });

  it('should remove refreshToken', () => {
    const value = 'test';

    jwtSecurity.refreshToken.value = value;
    jwtSecurity.refreshToken.removeValue();

    expect(jwtSecurity.refreshToken.value).toBe('');
  });

  it('should return false when token is invalid', () => {
    const value = 'test';

    jwtSecurity.accessToken.value = value;

    expect(jwtSecurity.accessToken.isValid()).toBe(false);
  });

  it('should return true when token is valid', () => {
    const secret_key = 'secret';
    const payload = {
      user_id: 150,
      username: 'test',
      exp: Math.floor(Date.now() / 1000) + 60 * 60, // expires in 1 hour
    };

    const token = jwt.sign(payload, secret_key);
    jwtSecurity.accessToken.value = token;

    expect(jwtSecurity.accessToken.isValid()).toBe(true);
  });

  it('should return false when token is expired', () => {
    const secret = 'secret';
    const payload = {
      user_id: 150,
      username: 'test',
      exp: Math.floor(Date.now() / 1000) - 60 * 60, // expired 1 hour ago
    };

    const token = jwt.sign(payload, secret);
    jwtSecurity.accessToken.value = token;

    expect(jwtSecurity.accessToken.isValid()).toBe(false);
  });
});
