import { AuthContext, AuthContextType } from '@/providers/AuthProvider';
import { useContext } from 'react';

/**
 * Custom hook to use the AuthContext
 * @returns {AuthContextType} The AuthContext
 */
const useAuth = (): AuthContextType => {
  const { auth, setAuth } = useContext<AuthContextType>(
    AuthContext as React.Context<AuthContextType>,
  );

  return {
    auth,
    setAuth,
  };
};

export default useAuth;
