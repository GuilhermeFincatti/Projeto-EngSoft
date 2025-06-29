import React, { useEffect, useState, useRef } from 'react'
import { StyleSheet, Text, View, TouchableOpacity, Image, BackHandler, Alert, ActivityIndicator } from 'react-native'
import MapView, { PROVIDER_GOOGLE, Marker } from 'react-native-maps'
import { useRouter } from 'expo-router'
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { ProfileImage } from '../components/ProfileImage'
import { apiService } from '../services/api'
import { ESALQ_REGION, ESALQ_BOUNDS } from '../constants/locations'

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

const home = () => {
  const router = useRouter()
  const insets = useSafeAreaInsets()
  const mapRef = useRef(null)
  const [nickname, setNickname] = useState('')
  const [discoveredCards, setDiscoveredCards] = useState([])
  const [loadingCards, setLoadingCards] = useState(true)

  useEffect(() => {
    AsyncStorage.getItem('nickname').then(nome => {
      if (nome) setNickname(nome)
    })
    loadDiscoveredCards()
  }, [])

  const loadDiscoveredCards = async () => {
    try {
      setLoadingCards(true)
      
      // Buscar coleção do usuário com timeout
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 8000)
      );
      
      const colecao = await Promise.race([
        apiService.getMinhaColecao(),
        timeoutPromise
      ]);
      
      // Filtrar apenas cartas que têm coordenadas
      const cartasComCoordenadas = colecao.filter(item => {
        const carta = item.carta
        return carta && carta.coordinates && 
               carta.coordinates.latitude && 
               carta.coordinates.longitude
      }).map(item => ({
        ...item.carta,
        quantidade: item.quantidade
      }))
      
      setDiscoveredCards(cartasComCoordenadas)
    } catch (error) {
      console.warn('Erro ao carregar cartas descobertas:', error.message);
      // Continuar execução mesmo com erro
      setDiscoveredCards([]);
    } finally {
      setLoadingCards(false)
    }
  }

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

    if (latitude < ESALQ_BOUNDS.LAT_MIN) { latitude = ESALQ_BOUNDS.LAT_MIN; changed = true }
    if (latitude > ESALQ_BOUNDS.LAT_MAX) { latitude = ESALQ_BOUNDS.LAT_MAX; changed = true }
    if (longitude < ESALQ_BOUNDS.LNG_MIN) { longitude = ESALQ_BOUNDS.LNG_MIN; changed = true }
    if (longitude > ESALQ_BOUNDS.LNG_MAX) { longitude = ESALQ_BOUNDS.LNG_MAX; changed = true }

    if (changed && mapRef.current) {
      mapRef.current.animateToRegion({
        ...region,
        latitude,
        longitude,
      }, 200)
    }
  }

  // Função para navegar para os detalhes da carta
  const handleCardPress = (carta) => {
    router.push(`/carta/${carta.qrcode}`)
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
        {/* Marcadores das cartas descobertas */}
        {discoveredCards.map((carta, idx) => (
          <Marker
            key={`discovered-${carta.qrcode}-${idx}`}
            coordinate={carta.coordinates}
            title={carta.nome || `Carta ${carta.qrcode}`}
            description={`Localização: ${carta.localizacao}`}
            onPress={() => handleCardPress(carta)}
          >
            <View style={styles.discoveredMarker}>
              <Image
                source={require('../assets/local.png')}
                style={{ width: 25, height: 25 }}
                resizeMode="contain"
              />
              <View style={styles.markerBadge}>
                <Text style={styles.markerBadgeText}>✓</Text>
              </View>
            </View>
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
        <ProfileImage size={32} style={styles.profileImageInButton} />
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
      
      {/* Indicador de carregamento das cartas */}
      {loadingCards && (
        <View style={styles.loadingIndicator}>
          <ActivityIndicator size="small" color="#007AFF" />
          <Text style={styles.loadingText}>Carregando cartas descobertas...</Text>
        </View>
      )}
      
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
  profileImageInButton: {
    marginRight: 8,
  },
  profileName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2e7d32',
  },
  discoveredMarker: {
    position: 'relative',
    alignItems: 'center',
    justifyContent: 'center',
  },
  markerBadge: {
    position: 'absolute',
    top: -5,
    right: -5,
    backgroundColor: '#4CAF50',
    borderRadius: 8,
    width: 16,
    height: 16,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#fff',
  },
  markerBadgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  loadingIndicator: {
    position: 'absolute',
    top: 100,
    left: 20,
    right: 20,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 8,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.15,
    shadowRadius: 4,
    shadowOffset: { width: 0, height: 2 },
  },
  loadingText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#666',
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