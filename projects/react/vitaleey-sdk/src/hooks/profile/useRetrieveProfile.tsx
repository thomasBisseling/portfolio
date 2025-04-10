import { Profile } from '@/types/models/profile';
import { useState } from 'react';

import profileService from '@/services/profile.service';

/**
 * Hook to retrieve a profile
 */
const useRetrieveProfile = () => {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const retrieve = (userId: string) => {
    setLoading(true);
    profileService
      .retrieveProfile(userId)
      .then((data) => {
        setProfile(data as Profile);
      })
      .catch((error) => {
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return { retrieve, loading, error, profile };
};

export default useRetrieveProfile;
