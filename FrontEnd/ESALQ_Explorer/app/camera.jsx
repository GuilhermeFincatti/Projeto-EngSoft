import { StyleSheet, Text, View, Alert, TouchableOpacity, Dimensions } from 'react-native'
import React, { useState, useEffect } from 'react'
import { CameraView, Camera } from 'expo-camera'
import { useRouter } from 'expo-router'
import { apiService, ApiError, NetworkError } from '../services/api'
import { Ionicons } from '@expo/vector-icons'

const { width, height } = Dimensions.get('window')

const CameraScreen = () => {
  const [hasPermission, setHasPermission] = useState(null)
  const [scanned, setScanned] = useState(false)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    getCameraPermissions()
  }, [])

  const getCameraPermissions = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync()
    setHasPermission(status === 'granted')
  }

  const handleBarCodeScanned = async ({ type, data }) => {
    if (scanned || loading) return
    
    setScanned(true)
    setLoading(true)

    try {
      // Adiciona a carta à coleção
      const result = await apiService.adicionarCartaColecao(data)
      
      let mensagem = `Parabéns! Você coletou a carta ${data}!`
      let titulo = '🎉 Carta Coletada!'
      
      // Verificar se houve ganho de XP
      if (result.xp_info) {
        const xpInfo = result.xp_info
        mensagem += `\n\n✨ +${xpInfo.xp_ganho} XP (${xpInfo.raridade})!`
        mensagem += `\n🎯 XP Total: ${xpInfo.xp_total}`
        mensagem += `\n⭐ Nível: ${xpInfo.nivel_atual}`
        
        if (xpInfo.level_up) {
          titulo = '🎊 Level Up!'
          mensagem += `\n\n🚀 Você subiu de nível!`
          mensagem += `\n👑 Novo ranking: ${xpInfo.ranking}`
        }
      }
      
      Alert.alert(
        titulo,
        mensagem,
        [
          {
            text: 'Ver Coleção',
            onPress: () => router.push('/colecao')
          },
          {
            text: 'Continuar Escaneando',
            onPress: resetScanner,
            style: 'default'
          }
        ]
      )
    } catch (error) {
      console.error('Erro ao coletar carta:', error)
      
      let errorMessage = 'Erro ao coletar carta. Tente novamente.'
      
      if (error instanceof ApiError) {
        if (error.status === 404) {
          errorMessage = 'QR Code não reconhecido. Esta carta não existe no sistema.'
        } else {
          errorMessage = error.getUserMessage()
        }
      } else if (error instanceof NetworkError) {
        errorMessage = 'Sem conexão. Verifique sua internet e tente novamente.'
      }
      
      Alert.alert('Erro', errorMessage, [
        {
          text: 'Tentar Novamente',
          onPress: resetScanner
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const resetScanner = () => {
    setScanned(false)
  }

  if (hasPermission === null) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Solicitando permissão da câmera...</Text>
      </View>
    )
  }

  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Sem acesso à câmera</Text>
        <Text style={styles.subMessage}>
          Vá até as configurações e permita o acesso à câmera para escanear QR codes
        </Text>
        <TouchableOpacity style={styles.button} onPress={getCameraPermissions}>
          <Text style={styles.buttonText}>Tentar Novamente</Text>
        </TouchableOpacity>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        facing="back"
        onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
        barcodeScannerSettings={{
          barcodeTypes: ['qr'],
        }}
      />
      
      {/* Overlay com frame de escaneamento - usando absolute positioning */}
      <View style={styles.overlay}>
        <View style={styles.topOverlay} />
        <View style={styles.middleRow}>
          <View style={styles.sideOverlay} />
          <View style={styles.scanFrame}>
            <View style={[styles.corner, styles.topLeft]} />
            <View style={[styles.corner, styles.topRight]} />
            <View style={[styles.corner, styles.bottomLeft]} />
            <View style={[styles.corner, styles.bottomRight]} />
          </View>
          <View style={styles.sideOverlay} />
        </View>
        <View style={styles.bottomOverlay}>
          <Text style={styles.instruction}>
            {loading ? 'Coletando carta...' : 'Aponte a câmera para o QR code'}
          </Text>
          <TouchableOpacity 
            style={styles.backButton} 
            onPress={() => router.back()}
          >
            <Ionicons name="arrow-back" size={24} color="#fff" />
            <Text style={styles.backButtonText}>Voltar</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  )
}

export default CameraScreen

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'transparent',
  },
  topOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  middleRow: {
    flexDirection: 'row',
    height: 250,
  },
  sideOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  scanFrame: {
    width: 250,
    height: 250,
    position: 'relative',
  },
  corner: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderColor: '#2e7d32',
    borderWidth: 4,
  },
  topLeft: {
    top: 0,
    left: 0,
    borderRightWidth: 0,
    borderBottomWidth: 0,
  },
  topRight: {
    top: 0,
    right: 0,
    borderLeftWidth: 0,
    borderBottomWidth: 0,
  },
  bottomLeft: {
    bottom: 0,
    left: 0,
    borderRightWidth: 0,
    borderTopWidth: 0,
  },
  bottomRight: {
    bottom: 0,
    right: 0,
    borderLeftWidth: 0,
    borderTopWidth: 0,
  },
  bottomOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingBottom: 50,
  },
  instruction: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 30,
    fontFamily: 'Montserrat-Regular',
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(46, 125, 50, 0.8)',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 16,
    marginLeft: 8,
    fontFamily: 'Montserrat-Regular',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
    fontSize: 18,
    color: '#fff',
    fontFamily: 'Montserrat-Regular',
  },
  subMessage: {
    textAlign: 'center',
    paddingHorizontal: 20,
    fontSize: 14,
    color: '#ccc',
    marginBottom: 30,
    fontFamily: 'Montserrat-Regular',
  },
  button: {
    backgroundColor: '#2e7d32',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    alignSelf: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
  },
})