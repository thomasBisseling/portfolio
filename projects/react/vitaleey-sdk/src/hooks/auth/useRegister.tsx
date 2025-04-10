const useRegister = () => {
  return {
    register: async (email: string, password: string) => {
      console.log('register', email, password);
    },
  };
};

export default useRegister;
