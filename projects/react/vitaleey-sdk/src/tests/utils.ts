import jwt from 'jsonwebtoken';

const JWT_SECRET = 'secret';

/**
 * Create a valid token with a given userId
 * @param userId
 * @returns a valid token
 */
const createValidToken = (userId: string) => {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: '1h' });
};

/**
 * Create an expired token with a given userId
 * @param userId
 * @returns an expired token
 */
const createExpiredToken = (userId: string) => {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: '1ms' });
};

export { createExpiredToken, createValidToken };
