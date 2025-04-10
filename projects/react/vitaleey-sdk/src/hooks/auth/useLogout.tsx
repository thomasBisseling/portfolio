import jwtSecurity from '@/security/jwt.security';
import useAuth from './useAuth';

const useLogout = () => {
  const { setAuth } = useAuth();

  const logout = () => {
    setAuth({
      isAuthenticated: false,
      user: null,
      token: '',
    });

    jwtSecurity.accessToken.value = '';
    jwtSecurity.refreshToken.value = '';
  };

  return logout;
};

export default useLogout;
