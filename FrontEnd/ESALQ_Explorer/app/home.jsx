import React from 'react'
import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native'
import MapView, { PROVIDER_GOOGLE } from 'react-native-maps'
import { useRouter } from 'expo-router'
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context'

const home = () => {
  const router = useRouter()
  const insets = useSafeAreaInsets()

  return (
    <SafeAreaView style={styles.container} edges={['top', 'left', 'right']}>
      {/* Mapa interativo cobrindo toda a tela */}
      <MapView
        style={StyleSheet.absoluteFill}
        provider={PROVIDER_GOOGLE}
        initialRegion={{
          latitude: -22.70930097156, // Exemplo: ESALQ
          longitude: -47.6318968724,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
      />

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
          source={require('../assets/favicon.png')} // Coloque uma imagem de perfil padrão em assets
          style={styles.profileImage}
        />
        <Text style={styles.profileName}>Seu Nome</Text>
      </TouchableOpacity>

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
            source={require('../assets/favicon.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerText}>Coleção</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.footerButton, styles.cameraButton]}
          onPress={() => router.push('/camera')}
        >
          <Image
            source={require('../assets/favicon.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerCameraText}>QR Code</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.footerButton}
          onPress={() => router.push('/missoes')}
        >
          <Image
            source={require('../assets/favicon.png')}
            style={styles.footerIcon}
          />
          <Text style={styles.footerText}>Missões</Text>
        </TouchableOpacity>
      </View>
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
    backgroundColor: '#fff',
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
    backgroundColor: 'rgba(255,255,255,0.95)',
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
})