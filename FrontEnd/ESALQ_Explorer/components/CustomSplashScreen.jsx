import React, { useEffect, useState } from 'react';
import { View, Image, StyleSheet, Animated, Dimensions, Text } from 'react-native';

const { width, height } = Dimensions.get('window');

export const CustomSplashScreen = ({ onFinish }) => {
  const fadeAnim = new Animated.Value(0);
  const scaleAnim = new Animated.Value(0.3);
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    // Animate logo appearance
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 50,
        friction: 3,
        useNativeDriver: true,
      }),
    ]).start();

    // Auto finish after 2.5 seconds
    const timer = setTimeout(() => {
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }).start(() => {
        onFinish();
      });
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  const handleImageError = (error) => {
    console.warn('Erro ao carregar imagem do splash screen:', error);
    setImageError(true);
  };

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.logoContainer,
          {
            opacity: fadeAnim,
            transform: [{ scale: scaleAnim }],
          },
        ]}
      >
        {!imageError ? (
          <>
            <Image
              source={require('../assets/Logo_ESALQ_Explorer_Sem_Texto.png')}
              style={styles.logo}
              resizeMode="contain"
              onError={handleImageError}
            />
            <Image
              source={require('../assets/Logo_ESALQ_Explorer_Texto.png')}
              style={styles.logoText}
              resizeMode="contain"
              onError={handleImageError}
            />
          </>
        ) : (
          <View style={styles.fallbackContainer}>
            <Text style={styles.fallbackTitle}>ESALQ Explorer</Text>
            <Text style={styles.fallbackSubtitle}>Carregando...</Text>
          </View>
        )}
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e0f2f1',
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    width: width * 0.6,
    height: width * 0.45,
    marginBottom: 20,
  },
  logoText: {
    width: width * 0.5,
    height: width * 0.2,
  },
  fallbackContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  fallbackTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 10,
    textAlign: 'center',
  },
  fallbackSubtitle: {
    fontSize: 16,
    color: '#4CAF50',
    textAlign: 'center',
  },
});

export default CustomSplashScreen;
