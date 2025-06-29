import { View, Text, StyleSheet, Image, ScrollView, ActivityIndicator } from 'react-native'
import { useLocalSearchParams } from 'expo-router'
import { cartas } from './cartas'
import React, { useState, useEffect } from 'react'
import { apiService } from '../../services/api'

export default function CartaDetalhe() {
  const { id } = useLocalSearchParams()
  const [carta, setCarta] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    carregarCarta()
  }, [id])

  const carregarCarta = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Primeiro tenta buscar da coleção do usuário
      try {
        const minhaColecao = await apiService.getMinhaColecao()
        const cartaColecao = minhaColecao.find(item => item.qrcode === id)
        
        if (cartaColecao && cartaColecao.carta) {
          const cartaData = {
            id: cartaColecao.qrcode,
            qrcode: cartaColecao.qrcode,
            nome: cartaColecao.carta.nome || `Carta ${cartaColecao.qrcode}`,
            tipo: cartaColecao.carta.raridade,
            raridade: cartaColecao.carta.raridade,
            descricao: cartaColecao.carta.descricao || cartaColecao.carta.localizacao || 'Carta misteriosa',
            imagem: cartaColecao.carta.imagem,
            audio: cartaColecao.carta.audio,
            localizacao: cartaColecao.carta.localizacao,
            quantidade: cartaColecao.quantidade
          }
          setCarta(cartaData)
          return
        }
      } catch (colecaoError) {
        console.warn('Erro ao buscar da coleção:', colecaoError)
      }
      
      // Se não encontrou na coleção, busca todas as cartas
      try {
        const todasCartas = await apiService.getCartas()
        const cartaEncontrada = todasCartas.find(c => c.qrcode === id)
        
        if (cartaEncontrada) {
          const cartaData = {
            id: cartaEncontrada.qrcode,
            qrcode: cartaEncontrada.qrcode,
            nome: cartaEncontrada.nome || `Carta ${cartaEncontrada.qrcode}`,
            tipo: cartaEncontrada.raridade,
            raridade: cartaEncontrada.raridade,
            descricao: cartaEncontrada.descricao || cartaEncontrada.localizacao || 'Carta misteriosa',
            imagem: cartaEncontrada.imagem,
            audio: cartaEncontrada.audio,
            localizacao: cartaEncontrada.localizacao
          }
          setCarta(cartaData)
          return
        }
      } catch (cartasError) {
        console.warn('Erro ao buscar cartas:', cartasError)
      }
      
      // Fallback para dados locais
      const cartaLocal = cartas.find(c => c.id === Number(id) || c.id === id)
      if (cartaLocal) {
        setCarta(cartaLocal)
      } else {
        setError('Carta não encontrada')
      }
      
    } catch (error) {
      console.error('Erro ao carregar carta:', error)
      setError('Erro ao carregar carta')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#2e7d32" />
        <Text style={styles.loadingText}>Carregando carta...</Text>
      </View>
    )
  }

  if (error || !carta) {
    return (
      <View style={styles.container}>
        <Text style={styles.naoEncontrada}>{error || 'Carta não encontrada.'}</Text>
      </View>
    )
  }

  const getTipoStyle = (tipo) => {
    switch (tipo) {
      case 'rara':
        return { backgroundColor: '#FFD700', color: '#7c6500' }
      case 'épica':
        return { backgroundColor: '#9932CC', color: '#fff' }
      case 'lendária':
        return { backgroundColor: '#FF4500', color: '#fff' }
      case 'incomum':
        return { backgroundColor: '#32CD32', color: '#fff' }
      default:
        return { backgroundColor: '#b2dfdb', color: '#2e7d32' }
    }
  }

  const getCardStyle = (tipo) => {
    switch (tipo) {
      case 'rara':
        return { backgroundColor: '#fffbe6', borderColor: '#FFD700' }
      case 'épica':
        return { backgroundColor: '#f8f0ff', borderColor: '#9932CC' }
      case 'lendária':
        return { backgroundColor: '#fff5ee', borderColor: '#FF4500' }
      case 'incomum':
        return { backgroundColor: '#f0fff0', borderColor: '#32CD32' }
      default:
        return { backgroundColor: '#e0f2f1', borderColor: '#2e7d32' }
    }
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <View style={[
          styles.cartaDetalhe,
          getCardStyle(carta.tipo)
        ]}>
          {/* Imagem da carta */}
          {carta.imagem && (
            <Image 
              source={{ uri: carta.imagem }} 
              style={styles.imagemCarta}
              resizeMode="cover"
            />
          )}
          
          <Text style={styles.numeroCarta}>
            {(carta.qrcode || carta.id || '').toString().replace('QR', '').padStart(2, '0')}
          </Text>
          <Text style={styles.nomeCarta}>{carta.nome}</Text>
          <View style={[
            styles.tipoCarta,
            getTipoStyle(carta.tipo)
          ]}>
            <Text style={[styles.tipoTexto, { color: getTipoStyle(carta.tipo).color }]}>
              {carta.tipo?.toUpperCase() || 'COMUM'}
            </Text>
          </View>
          <Text style={styles.descricao}>{carta.descricao}</Text>
          
          {/* Informações adicionais */}
          {carta.localizacao && (
            <Text style={styles.localizacao}>📍 {carta.localizacao}</Text>
          )}
          
          {carta.quantidade && (
            <Text style={styles.quantidade}>Quantidade: {carta.quantidade}</Text>
          )}
        </View>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  cartaDetalhe: {
    width: 300,
    minHeight: 400,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    elevation: 4,
    borderWidth: 3,
    marginBottom: 20,
  },
  imagemCarta: {
    width: 200,
    height: 120,
    borderRadius: 12,
    marginBottom: 16,
  },
  numeroCarta: {
    fontSize: 48,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 8,
  },
  nomeCarta: {
    fontSize: 24,
    fontFamily: 'Montserrat-ExtraBold',
    color: '#2e7d32',
    marginBottom: 12,
    textAlign: 'center',
  },
  tipoCarta: {
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 12,
    marginBottom: 16,
  },
  tipoTexto: {
    fontSize: 16,
    fontFamily: 'Montserrat-Bold',
    letterSpacing: 2,
  },
  descricao: {
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
    color: '#555',
    textAlign: 'center',
    marginTop: 8,
    lineHeight: 22,
  },
  localizacao: {
    fontSize: 14,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    textAlign: 'center',
    marginTop: 12,
    fontStyle: 'italic',
  },
  quantidade: {
    fontSize: 14,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    textAlign: 'center',
    marginTop: 8,
  },
  loadingText: {
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
    color: '#2e7d32',
    marginTop: 10,
  },
  naoEncontrada: {
    fontSize: 20,
    color: '#c00',
    fontFamily: 'Montserrat-Bold',
    textAlign: 'center',
  },
})