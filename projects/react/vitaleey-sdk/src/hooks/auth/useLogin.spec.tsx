import authService from '@/services/auth.service';
import TestWrapper from '@/tests/TestWrapper';
import { createValidToken } from '@/tests/utils';
import { ResponseError } from '@/types/common';
import { act, renderHook, waitFor } from '@testing-library/react';
import useLogin from './useLogin';

describe('useLogin', () => {
  it('should return tokens for the user', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
    };

    const mockTokens = {
      token: createValidToken(mockUser.id.toString()),
      refreshToken: createValidToken(mockUser.id.toString()),
    };

    jest.spyOn(authService, 'login').mockResolvedValueOnce(mockTokens);
    jest.spyOn(authService, 'currentUser').mockResolvedValueOnce(mockUser);

    const { result } = renderHook(() => useLogin(), { wrapper: TestWrapper } as any);
    let { login, auth } = result.current;

    act(() => {
      login('test@example.com', 'password');
    });

    await waitFor(() => {
      ({ auth } = result.current);
      expect(auth.isAuthenticated).toEqual(true);
    });
  });

  it('should return an error if the credentials are invalid', async () => {
    const mockError: ResponseError = {
      error: {
        message: 'Something went wrong',
        code: 'ERROR_101',
      },
    };

    jest.spyOn(authService, 'login').mockRejectedValueOnce(mockError);

    const { result } = renderHook(() => useLogin(), { wrapper: TestWrapper } as any);
    let { login, error } = result.current;

    act(() => {
      login('test@example.com', 'password');
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toEqual(mockError);
    });
  });

  it('should return an error if the token response is invalid', async () => {
    const mockTokens = {
      token: '',
      refreshToken: '',
    };

    jest.spyOn(authService, 'login').mockResolvedValue(mockTokens);

    const { result } = renderHook(() => useLogin(), { wrapper: TestWrapper } as any);
    let { login, error } = result.current;

    act(() => {
      login('test@example.com', 'password');
    });

    await waitFor(() => {
      ({ error } = result.current);
      expect(error).toEqual({
        error: {
          message: 'Invalid token response',
          code: 'INVALID_TOKEN',
        },
      });
    });
  });

  it('should return an error if token are set but unable to request user', async () => {
    jest.spyOn(authService, 'currentUser').mockRejectedValueOnce({
      error: {
        message: 'Something went wrong',
        code: 'ERROR_101',
      },
    });

    const mockTokens = {
      token: createValidToken('1'),
      refreshToken: createValidToken('1'),
    };

    jest.spyOn(authService, 'login').mockResolvedValue(mockTokens);

    const { result } = renderHook(() => useLogin(), { wrapper: TestWrapper } as any);
    let { login, auth } = result.current;

    act(() => {
      login('test@example.com', 'password');
    });

    await waitFor(() => {
      ({ auth } = result.current);
      expect(auth).toEqual({
        isAuthenticated: false,
        user: null,
        token: '',
      });
    });
  });
});
