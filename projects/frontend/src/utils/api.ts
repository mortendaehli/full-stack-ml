import { BACKEND_URL } from '../config';

export const getHealth = async () => {
  const response = await fetch(BACKEND_URL + '/health');

  const data = await response.json();

  if (data.message) {
    return data.message;
  }

  return Promise.reject('Failed to get message from backend');
};
