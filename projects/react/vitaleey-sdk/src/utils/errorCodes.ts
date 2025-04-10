const errorCodes = {
  '101': 'Email already in use',
  '102': 'Invalid email',
  '103': 'User not found',
  '104': 'Wrong password',
  '105': 'Weak password',
  '106': 'Too many login attempts',
  '107': 'Recipe not found',
  '201': 'Recipe already exists',
  '203': 'Invalid recipe',
  '204': 'Invalid ingredient',
};

export const getErrorMessage = (code: string) => {
  const errorPrefix = 'ERROR_';

  if (!code.startsWith(errorPrefix)) {
    return 'Unknown error';
  }

  const errorCode = code.split(errorPrefix)[1] as keyof typeof errorCodes;
  if (errorCode in errorCodes) {
    return errorCodes[errorCode];
  }

  return 'Unknown error';
};
