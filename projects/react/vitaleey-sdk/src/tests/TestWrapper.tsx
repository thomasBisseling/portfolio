import AuthProvider from '@/providers/AuthProvider';
import React from 'react';

const TestWrapper = ({ children }: { children: React.ReactNode }) => {
  return <AuthProvider>{children}</AuthProvider>;
};

export default TestWrapper;
