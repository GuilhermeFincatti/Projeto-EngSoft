import { StyleSheet, Text, View, FlatList, TouchableOpacity, Image } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useRouter } from 'expo-router'
import { cartas } from './carta/cartas' // Fallback local
import AsyncStorage from '@react-native-async-storage/async-storage'
import { apiService, ApiError, NetworkError } from '../services/api'

const colecao = () => {
  const [cartasColetadas, setCartasColetadas] = useState([])
  const [cartasDisponiveis, setCartasDisponiveis] = useState(cartas) // Fallback local
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    try {
      setLoading(true)
      
      // Carrega cartas do servidor
      try {
        const cartasServidor = await apiService.getCartas()
        // Mapeia a estrutura do backend para o formato esperado pelo frontend
        const cartasFormatadas = cartasServidor.map(carta => ({
          id: carta.qrcode,
          qrcode: carta.qrcode,
          nome: carta.nome || `Carta ${carta.qrcode}`,
          tipo: carta.raridade,
          raridade: carta.raridade,
          descricao: carta.descricao || carta.localizacao || 'Carta misteriosa',
          imagem: carta.imagem,
          audio: carta.audio,
          localizacao: carta.localizacao
        }))
        setCartasDisponiveis(cartasFormatadas)
      } catch (error) {
        console.warn('Erro ao carregar cartas do servidor, usando dados locais:', error)
        // Mantém o fallback local em caso de erro
      }

      // Carrega coleção do usuário
      try {
        const minhaColecao = await apiService.getMinhaColecao()
        console.log('Minha coleção carregada:', minhaColecao)
        
        // A API retorna objetos com { qrcode, quantidade, carta: {...} }
        const idsColetados = minhaColecao.map(item => item.qrcode)
        setCartasColetadas(idsColetados)
        
        // Salva no AsyncStorage como backup
        await AsyncStorage.setItem('cartasColetadas', JSON.stringify(idsColetados))
        
        console.log('Cartas coletadas definidas:', idsColetados)
        
      } catch (error) {
        console.warn('Erro ao carregar coleção do servidor, usando dados locais:', error)
        // Carrega do AsyncStorage como backup
        try {
          const cartasLocais = await AsyncStorage.getItem('cartasColetadas')
          if (cartasLocais) {
            const idsLocais = JSON.parse(cartasLocais)
            setCartasColetadas(idsLocais)
            console.log('Cartas coletadas do storage local:', idsLocais)
          }
        } catch (asyncError) {
          console.error('Erro ao carregar dados locais:', asyncError)
        }
      }
      
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  // Função para adicionar cartas de exemplo (para teste)
  const adicionarCartasExemplo = async () => {
    try {
      const cartasExemplo = ['QR001', 'QR003', 'QR005', 'QR007', 'QR009'] // QRCodes de exemplo
      
      // Tenta adicionar no servidor
      for (const qrcode of cartasExemplo) {
        try {
          await apiService.adicionarCartaColecao(qrcode)
        } catch (error) {
          console.warn(`Erro ao adicionar carta ${qrcode} no servidor:`, error)
        }
      }
      
      // Recarrega dados do servidor
      await carregarDados()
    } catch (error) {
      console.error('Erro ao adicionar cartas de exemplo:', error)
    }
  }

  // Função para limpar coleção (para teste)
  const limparColecao = async () => {
    try {
      await apiService.limparColecao()
      // Recarrega dados do servidor
      await carregarDados()
    } catch (error) {
      console.error('Erro ao limpar coleção:', error)
      // Fallback local se servidor não disponível
      setCartasColetadas([])
      await AsyncStorage.setItem('cartasColetadas', JSON.stringify([]))
    }
  }

  const getCartaStyle = (item, coletada) => {
    const baseStyle = [styles.carta]
    
    if (coletada) {
      baseStyle.push(styles.cartaColetada)
      
      // Adiciona estilo específico baseado no tipo
      switch (item.tipo) {
        case 'rara':
          baseStyle.push(styles.cartaRara)
          break
        case 'épica':
          baseStyle.push(styles.cartaEpica)
          break
        case 'lendária':
          baseStyle.push(styles.cartaLendaria)
          break
        case 'incomum':
          baseStyle.push(styles.cartaIncomum)
          break
      }
    }
    
    return baseStyle
  }

  const getStatusText = (item, coletada) => {
    if (!coletada) return '???'
    
    switch (item.tipo) {
      case 'comum': return 'Comum'
      case 'incomum': return 'Incomum'
      case 'rara': return 'Rara'
      case 'épica': return 'Épica'
      case 'lendária': return 'Lendária'
      default: return 'Comum'
    }
  }

  const renderCarta = ({ item }) => {
    const coletada = cartasColetadas.includes(item.id || item.qrcode)
    const cartaData = coletada ? cartasDisponiveis.find(c => (c.id || c.qrcode) === (item.id || item.qrcode)) || item : item
    
    console.log(`Renderizando carta ${item.qrcode}, coletada: ${coletada}`)
    
    return (
      <TouchableOpacity
        style={getCartaStyle(cartaData, coletada)}
        onPress={coletada ? () => router.push(`/carta/${item.id || item.qrcode}`) : undefined}
        activeOpacity={coletada ? 0.7 : 1}
      >
        {/* Imagem da carta (se coletada e tiver imagem) */}
        {coletada && cartaData.imagem && (
          <Image 
            source={{ uri: cartaData.imagem }} 
            style={styles.imagemCarta}
            resizeMode="cover"
          />
        )}
        
        {/* Número da carta */}
        <Text style={[styles.numeroCarta, coletada && styles.numeroCartaColetada]}>
          {(item.id || item.qrcode || '').toString().replace('QR', '').replace('0', '').padStart(2, '0')}
        </Text>
        
        {/* Nome da carta (se coletada) */}
        {coletada && cartaData.nome && (
          <Text style={[styles.nomeCarta, styles.nomeCartaColetada]}>
            {cartaData.nome}
          </Text>
        )}
        
        {/* Status/Raridade */}
        <Text style={[styles.statusCarta, coletada && styles.statusCartaColetada]}>
          {getStatusText(cartaData, coletada)}
        </Text>
      </TouchableOpacity>
    )
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Coleção de Cartas</Text>
      <Text style={styles.subtitle}>Complete sua coleção!</Text>
      
      {/* Botões de teste - remova em produção */}
      <View style={styles.testButtons}>
        <TouchableOpacity style={styles.testButton} onPress={adicionarCartasExemplo}>
          <Text style={styles.testButtonText}>Adicionar Cartas</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.testButton} onPress={limparColecao}>
          <Text style={styles.testButtonText}>Limpar Coleção</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={cartasDisponiveis}
        renderItem={renderCarta}
        keyExtractor={item => (item.id || item.qrcode || Math.random()).toString()}
        numColumns={3}
        contentContainerStyle={styles.grid}
        showsVerticalScrollIndicator={false}
        refreshing={loading}
        onRefresh={carregarDados}
      />
    </View>
  )
}

export default colecao

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: 40,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontFamily: 'Montserrat-ExtraBold',
    color: '#2e7d32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 18,
    fontFamily: 'Montserrat-Regular',
    color: '#555',
    marginBottom: 20,
  },
  grid: {
    alignItems: 'center',
    paddingBottom: 30,
  },
  carta: {
    backgroundColor: '#e0f2f1',
    borderColor: '#2e7d32',
    borderWidth: 2,
    borderRadius: 16,
    width: 90,
    height: 130,
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    padding: 4,
  },
  cartaColetada: {
    backgroundColor: '#2e7d32',
    borderColor: '#388e3c',
  },
  cartaRara: {
    borderWidth: 3,
    borderColor: '#FFD700',
    backgroundColor: '#fff8dc',
  },
  cartaIncomum: {
    borderWidth: 3,
    borderColor: '#32CD32',
    backgroundColor: '#f0fff0',
  },
  cartaEpica: {
    borderWidth: 3,
    borderColor: '#9932CC',
    backgroundColor: '#f8f0ff',
  },
  cartaLendaria: {
    borderWidth: 3,
    borderColor: '#FF4500',
    backgroundColor: '#fff5ee',
  },
  numeroCarta: {
    fontSize: 24,
    color: '#333',
    fontFamily: 'Montserrat-Bold',
    marginBottom: 4,
  },
  numeroCartaColetada: {
    color: '#fff',
  },
  statusCarta: {
    fontSize: 12,
    color: '#666',
    fontFamily: 'Montserrat-Regular',
    textAlign: 'center',
  },
  statusCartaColetada: {
    color: '#fff',
    fontWeight: 'bold',
  },
  imagemCarta: {
    width: 70,
    height: 40,
    borderRadius: 6,
    marginBottom: 4,
  },
  nomeCarta: {
    fontSize: 8,
    color: '#333',
    fontFamily: 'Montserrat-Regular',
    textAlign: 'center',
    marginBottom: 2,
    paddingHorizontal: 2,
  },
  nomeCartaColetada: {
    color: '#fff',
    fontWeight: 'bold',
  },
  testButtons: {
    flexDirection: 'row',
    marginBottom: 20,
    gap: 10,
  },
  testButton: {
    backgroundColor: '#2e7d32',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 8,
  },
  testButtonText: {
    color: '#fff',
    fontSize: 12,
    fontFamily: 'Montserrat-Regular',
  },
})