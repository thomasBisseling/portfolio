import profileService from '@/services/profile.service';
import { Profile } from '@/types/models/profile';
import { useState } from 'react';

/**
 * Hook to update a profile
 */
const useUpdateProfile = () => {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const update = (userId: string, data: Profile) => {
    setLoading(true);
    profileService
      .updateProfile(userId, data)
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

  return { update, loading, error, profile };
};

export default useUpdateProfile;
