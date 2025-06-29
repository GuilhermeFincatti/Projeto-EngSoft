import React from 'react';
import { Image, StyleSheet, ActivityIndicator, View } from 'react-native';
import { useProfileImage } from '../hooks/useProfileImage';

/**
 * Componente reutilizável para exibir a foto de perfil do usuário
 * Garante consistência em toda a aplicação
 */
export const ProfileImage = ({ 
  size = 40, 
  style = {}, 
  showLoader = false,
  borderRadius = null 
}) => {
  const { profileImage, loading } = useProfileImage();
  
  const finalBorderRadius = borderRadius !== null ? borderRadius : size / 2;
  
  const imageStyle = {
    width: size,
    height: size,
    borderRadius: finalBorderRadius,
    ...style
  };

  if (loading && showLoader) {
    return (
      <View style={[imageStyle, styles.loaderContainer]}>
        <ActivityIndicator size="small" color="#007AFF" />
      </View>
    );
  }

  return (
    <Image
      source={
        profileImage
          ? { uri: profileImage }
          : require('../assets/perfil.png')
      }
      style={imageStyle}
      resizeMode="cover"
    />
  );
};

const styles = StyleSheet.create({
  loaderContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f0f0f0'
  }
});

export default ProfileImage;
