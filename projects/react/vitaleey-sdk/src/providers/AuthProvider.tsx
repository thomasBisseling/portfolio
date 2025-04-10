import authService from '@/services/auth.service';
import { User } from '@/types/models/user';
import React, { createContext, useEffect, useRef, useState } from 'react';

export type AuthType = {
  isAuthenticated: boolean;
  user: User | null;
  token: string;
};

export type AuthContextType = {
  auth: AuthType;
  setAuth: React.Dispatch<React.SetStateAction<AuthType>>;
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

type AuthProviderProps = {
  children: React.ReactNode;
};

const AuthProvider = ({ children }: AuthProviderProps) => {
  const [auth, setAuth] = useState<AuthType>({
    isAuthenticated: false,
    user: null,
    token: '',
  });
  const isUserMounted = useRef(false);

  useEffect(() => {
    if (auth.isAuthenticated && !isUserMounted.current) {
      isUserMounted.current = true;
      authService
        .currentUser()
        .then((data) => {
          if (data === null) {
            setAuth({
              isAuthenticated: false,
              user: null,
              token: '',
            });
            return;
          }

          setAuth({
            isAuthenticated: true,
            user: data as User,
            token: auth.token,
          });
        })
        .catch(() => {
          setAuth({
            isAuthenticated: false,
            user: null,
            token: '',
          });
        });
    }
  }, [auth, isUserMounted]);

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>{children}</AuthContext.Provider>
  );
};

export default AuthProvider;
