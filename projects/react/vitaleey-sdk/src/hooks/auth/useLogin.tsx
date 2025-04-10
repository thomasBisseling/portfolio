import { AuthType } from '@/providers/AuthProvider';
import jwtSecurity from '@/security/jwt.security';
import authService from '@/services/auth.service';
import { ResponseError } from '@/types/common';
import { Token } from '@/types/models/user';
import { useState } from 'react';
import useAuth from './useAuth';

type useLoginType = {
  login: (email: string, password: string) => void;
  auth: AuthType;
  loading: boolean;
  error: ResponseError | null;
};

/**
 * Custom hook to handle the login logic
 * @returns {useLoginType} The login object
 */
const useLogin = (): useLoginType => {
  const { auth, setAuth } = useAuth();
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<ResponseError | null>(null);

  const login = (email: string, password: string) => {
    setLoading(true);
    authService
      .login(email, password)
      .then((data) => {
        const tokens = data as Token;
        if (!tokens.token || !tokens.refreshToken) {
          setError({
            error: {
              message: 'Invalid token response',
              code: 'INVALID_TOKEN',
            },
          });
          return;
        }

        jwtSecurity.accessToken.value = tokens.token;
        jwtSecurity.refreshToken.value = tokens.refreshToken;
        setAuth({
          isAuthenticated: true,
          user: null,
          token: jwtSecurity.accessToken.value,
        });
      })
      .catch((e: ResponseError) => {
        setError(e);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return {
    login,
    auth,
    loading,
    error,
  };
};

export default useLogin;
