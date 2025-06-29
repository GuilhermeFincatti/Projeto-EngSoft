import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from '../services/api';

/**
 * Hook personalizado para gerenciar a foto de perfil do usuário de forma consistente
 */
export const useProfileImage = () => {
  const [profileImage, setProfileImage] = useState(null);
  const [loading, setLoading] = useState(true);

  // Carregar foto de perfil ao inicializar
  useEffect(() => {
    loadProfileImage();
  }, []);

  const loadProfileImage = async () => {
    try {
      setLoading(true);
      
      // 1. Primeiro, tentar buscar do backend (fonte de verdade)
      const nickname = await AsyncStorage.getItem('nickname');
      if (nickname) {
        try {
          const profileStats = await apiService.getProfileStats(nickname);
          if (profileStats.success && profileStats.data.fotoperfil) {
            const backendImage = profileStats.data.fotoperfil;
            setProfileImage(backendImage);
            // Sincronizar com AsyncStorage
            await AsyncStorage.setItem('profileImage', backendImage);
            setLoading(false);
            return;
          }
        } catch (apiError) {
          console.warn('Erro ao buscar foto do backend:', apiError);
        }
      }
      
      // 2. Se não encontrou no backend, usar AsyncStorage como fallback
      const localImage = await AsyncStorage.getItem('profileImage');
      if (localImage) {
        setProfileImage(localImage);
      }
      
    } catch (error) {
      console.error('Erro ao carregar foto de perfil:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateProfileImage = async (newImageUri) => {
    try {
      // 1. Atualizar estado local imediatamente
      setProfileImage(newImageUri);
      
      // 2. Salvar no AsyncStorage
      await AsyncStorage.setItem('profileImage', newImageUri);
      
      // 3. Fazer upload para o backend
      const nickname = await AsyncStorage.getItem('nickname');
      if (nickname) {
        try {
          const uploadResult = await apiService.uploadProfilePhoto(nickname, newImageUri);
          if (uploadResult.success) {
            const backendImageUrl = uploadResult.data.fotoperfil || uploadResult.data.foto_url;
            if (backendImageUrl) {
              // 4. Atualizar com a URL final do backend
              setProfileImage(backendImageUrl);
              await AsyncStorage.setItem('profileImage', backendImageUrl);
            }
            return { success: true };
          } else {
            throw new Error(uploadResult.error || 'Erro ao fazer upload');
          }
        } catch (uploadError) {
          console.error('Erro no upload para o backend:', uploadError);
          return { success: false, error: uploadError.message };
        }
      }
      
      return { success: true };
    } catch (error) {
      console.error('Erro ao atualizar foto de perfil:', error);
      return { success: false, error: error.message };
    }
  };

  const refreshProfileImage = async () => {
    await loadProfileImage();
  };

  return {
    profileImage,
    loading,
    updateProfileImage,
    refreshProfileImage
  };
};
