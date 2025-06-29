import React, { useEffect, useState, useRef } from 'react'
import { StyleSheet, Text, View, TouchableOpacity, Image, BackHandler, Alert } from 'react-native'
import MapView, { PROVIDER_GOOGLE, Marker } from 'react-native-maps'
import { useRouter } from 'expo-router'
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context'
import AsyncStorage from '@react-native-async-storage/async-storage'

// Região aproximada da ESALQ para o mapa
const ESALQ_REGION = {
  latitude: -22.7093,
  longitude: -47.6319,
  latitudeDelta: 0.005,
  longitudeDelta: 0.005,
}

// Limites aproximados da ESALQ
const LAT_MIN = -22.7100
const LAT_MAX = -22.7000
const LNG_MIN = -47.6430
const LNG_MAX = -47.6200

// Estilo do mapa para esconder POIs e transporte público
const mapStyle = [
  {
    featureType: 'poi',
    stylers: [{ visibility: 'off' }]
  },
  {
    featureType: 'transit',
    stylers: [{ visibility: 'off' }]
  }
]

// Lista de locais com QR Codes (Depois será integrado com o backend)
const qrLocations = [
  { latitude: -22.7085, longitude: -47.6305 },
  { latitude: -22.7090, longitude: -47.6320 },
];

const home = () => {
  const router = useRouter()
  const insets = useSafeAreaInsets()
  const mapRef = useRef(null)
  const [nickname, setNickname] = useState('')
  const [profileImage, setProfileImage] = useState(null)

  useEffect(() => {
    AsyncStorage.getItem('nickname').then(nome => {
      if (nome) setNickname(nome)
    })
    AsyncStorage.getItem('profileImage').then(img => {
      if (img) setProfileImage(img)
    })
  }, [])

  useEffect(() => {
    const onBackPress = () => {
      Alert.alert(
        'Sair do aplicativo',
        'Você realmente deseja sair?',
        [
          { text: 'Cancelar', style: 'cancel' },
          { text: 'Sim', onPress: () => BackHandler.exitApp() }
        ]
      )
      return true // impede o comportamento padrão
    }

    const backHandler = BackHandler.addEventListener('hardwareBackPress', onBackPress)

    return () => backHandler.remove()
  }, [])

  // Função para manter o usuário dentro da área da ESALQ
  const handleRegionChange = (region) => {
    let { latitude, longitude } = region
    let changed = false

    if (latitude < LAT_MIN) { latitude = LAT_MIN; changed = true }
    if (latitude > LAT_MAX) { latitude = LAT_MAX; changed = true }
    if (longitude < LNG_MIN) { longitude = LNG_MIN; changed = true }
    if (longitude > LNG_MAX) { longitude = LNG_MAX; changed = true }

    if (changed && mapRef.current) {
      mapRef.current.animateToRegion({
        ...region,
        latitude,
        longitude,
      }, 200)
    }
  }

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      {/* Mapa interativo cobrindo toda a tela */}
      <MapView
        ref={mapRef}
        style={StyleSheet.absoluteFill}
        provider={PROVIDER_GOOGLE}
        initialRegion={ESALQ_REGION}
        minZoomLevel={15} // Impede de afastar muito
        maxZoomLevel={20} // Impede de aproximar demais
        onRegionChangeComplete={handleRegionChange}
        customMapStyle={mapStyle} // Aplica o estilo do mapa
      >
        {qrLocations.map((loc, idx) => (
          <Marker
            key={idx}
            coordinate={loc}
            title="QR Code aqui!"
            description="Escaneie para ganhar uma carta."
          >
            <Image
              source={require('../assets/local.png')}
              style={{ width: 25, height: 25 }}
              resizeMode="contain"
            />
          </Marker>
        ))}
      </MapView>

      {/* Botão de perfil no canto superior esquerdo, respeitando o safe area */}
      <TouchableOpacity
        style={[
          styles.profileButton,
          { top: insets.top + 16 } // 16 é um espaçamento extra opcional
        ]}
        onPress={() => router.push('/perfil')}
        activeOpacity={0.7}
      >
        <Image
          source={
            profileImage
              ? { uri: profileImage }
              : require('../assets/perfil.png')
          }
          style={styles.profileImage}
        />
        <Text style={styles.profileName}>{nickname || 'Seu Nome'}</Text>
      </TouchableOpacity>

      {/* Botões laterais para novas funcionalidades */}
      <View style={styles.sideButtonsContainer}>
        <TouchableOpacity
          style={styles.sideButton}
          onPress={() => router.push('/leaderboard')}
        >
          <Text style={styles.sideButtonIcon}>🏆</Text>
          <Text style={styles.sideButtonText}>Ranking</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.sideButton}
          onPress={() => router.push('/amigos')}
        >
          <Text style={styles.sideButtonIcon}>👥</Text>
          <Text style={styles.sideButtonText}>Amigos</Text>
        </TouchableOpacity>
      </View>

      {/* Rodapé com botões, respeitando o safe area */}
      <View style={[
        styles.footerButtonPosition,
        { paddingBottom: insets.bottom > 0 ? insets.bottom : 16 }
      ]}>
        <TouchableOpacity
          style={styles.footerButton}
          onPress={() => router.push('/colecao')}
        >
          <Image
            source={require('../assets/colecao.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerText}>Coleção</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.footerButton, styles.cameraButton]}
          onPress={() => router.push('/camera')}
        >
          <Image
            source={require('../assets/camera.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerCameraText}>Câmera</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.footerButton}
          onPress={() => router.push('/missoes')}
        >
          <Image
            source={require('../assets/missoes.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerText}>Missões</Text>
        </TouchableOpacity>
      </View>
      
      {/* Botão de teste QR - apenas para desenvolvimento */}
      <TouchableOpacity
        style={styles.testQRButton}
        onPress={() => router.push('/test-qr')}
      >
        <Text style={styles.testQRText}>🧪</Text>
      </TouchableOpacity>
    </SafeAreaView>
  )
}

export default home

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e0f2f1',
  },
  profileButton: {
    position: 'absolute',
    left: 20,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: 30,
    padding: 8,
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.15,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  profileImage: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 8,
  },
  profileName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2e7d32',
  },
  sideButtonsContainer: {
    position: 'absolute',
    right: 16,
    top: '50%',
    transform: [{ translateY: -60 }],
  },
  sideButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 25,
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  sideButtonIcon: {
    fontSize: 20,
  },
  sideButtonText: {
    fontSize: 8,
    color: '#333',
    fontWeight: '600',
    marginTop: 2,
  },
  footerButtonPosition: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 30,
    backgroundColor: 'rgba(255,255,255, 0.9)',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    height: 120,
    elevation: 10,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: -2 },
  },
  footerButton: {
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
  },
  cameraButton: {
    backgroundColor: '#2e7d32',
    borderRadius: 40,
    width: 70,
    height: 70,
    marginHorizontal: 10,
    marginTop: -10,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 6,
  },
  footerCameraText: {
    fontSize: 12,
    color: '#fff',
    fontWeight: '600',
  },
  footerIcon: {
    width: 32,
    height: 32,
    marginBottom: 4,
  },
  footerText: {
    fontSize: 12,
    color: '#2e7d32',
    fontWeight: '600',
  },
  testQRButton: {
    position: 'absolute',
    top: 120,
    right: 20,
    backgroundColor: '#FF9800',
    width: 50,
    height: 50,
    borderRadius: 25,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  testQRText: {
    color: '#fff',
    fontSize: 16,
  },
})