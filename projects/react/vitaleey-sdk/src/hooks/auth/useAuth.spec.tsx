import authService from '@/services/auth.service';
import TestWrapper from '@/tests/TestWrapper';
import { act, renderHook, waitFor } from '@testing-library/react';
import useAuth from './useAuth';

describe('useAuth', () => {
  it('should return tokens for the user', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
    };

    const mockAuth = {
      token: '123',
      isAuthenticated: true,
      user: mockUser,
    };

    jest.spyOn(authService, 'currentUser').mockResolvedValueOnce(mockUser);

    const { result } = renderHook(() => useAuth(), { wrapper: TestWrapper } as any);
    let { setAuth, auth } = result.current;

    act(() => {
      setAuth(mockAuth);
    });

    await waitFor(() => {
      ({ auth } = result.current);
      expect(auth).toEqual(mockAuth);
    });
  });
});
