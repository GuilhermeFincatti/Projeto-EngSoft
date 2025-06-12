import React from 'react'
import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native'
import MapView, { PROVIDER_GOOGLE } from 'react-native-maps'
import { useRouter } from 'expo-router'

const home = () => {
  const router = useRouter()

  return (
    <View style={styles.container}>
      {/* Mapa interativo cobrindo toda a tela */}
      <MapView
        style={StyleSheet.absoluteFill}
        provider={PROVIDER_GOOGLE}
        initialRegion={{
          latitude: -22.709300971569792, // Exemplo: ESALQ
          longitude: -47.63189687243349,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
      />

      {/* Botão de perfil no canto superior esquerdo */}
      <TouchableOpacity
        style={styles.profileButton}
        onPress={() => router.push('/perfil')}
        activeOpacity={0.7}
      >
        <Image
          source={require('../../assets/favicon.png')} // Coloque uma imagem de perfil padrão em assets
          style={styles.profileImage}
        />
        <Text style={styles.profileName}>Seu Nome</Text>
      </TouchableOpacity>
    </View>
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
    top: 40,
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
})