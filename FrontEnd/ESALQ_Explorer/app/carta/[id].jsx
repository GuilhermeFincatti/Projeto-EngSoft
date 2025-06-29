import { View, Text, StyleSheet, Image } from 'react-native'
import { useLocalSearchParams } from 'expo-router'
import { cartas } from './cartas'
import React from 'react'

export default function CartaDetalhe() {
  const { id } = useLocalSearchParams()
  const carta = cartas.find(c => c.id === Number(id))

  if (!carta) {
    return (
      <View style={styles.container}>
        <Text style={styles.naoEncontrada}>Carta não encontrada.</Text>
      </View>
    )
  }

  // Seleciona o estilo da carta conforme o tipo
  const getCartaStyle = tipo => {
    switch (tipo) {
      case 'rara':
        return styles.cartaRara
      case 'épica':
        return styles.cartaEpica
      case 'lendária':
        return styles.cartaLendaria
      default:
        return styles.cartaComum
    }
  }

  // Seleciona o estilo do tipo conforme o tipo
  const getTipoStyle = tipo => {
    switch (tipo) {
      case 'rara':
        return styles.tipoRara
      case 'épica':
        return styles.tipoEpica
      case 'lendária':
        return styles.tipoLendaria
      default:
        return styles.tipoComum
    }
  }

  return (
    <View style={styles.container}>
      <View style={[styles.cartaDetalhe, getCartaStyle(carta.tipo)]}>
        {/* Exibe a imagem se existir */}
        {carta.imagem && (
          <Image
            source={carta.imagem}
            style={{ width: 120, height: 120, borderRadius: 12}}
            resizeMode="cover"
          />
        )}
        <Text style={styles.numeroCarta}>{carta.id.toString().padStart(2, '0')}</Text>
        <Text style={styles.nomeCarta}>{carta.nome}</Text>
        <Text style={[styles.tipoCarta, getTipoStyle(carta.tipo)]}>
          {carta.tipo ? carta.tipo.toUpperCase() : ''}
        </Text>
        <Text style={styles.descricao}>{carta.descricao}</Text>
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  cartaDetalhe: {
    width: 320,
    height: 420,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    elevation: 4,
    borderWidth: 3,
    marginBottom: 20,
  },
  cartaComum: {
    backgroundColor: '#e0f2f1',
    borderColor: '#2e7d32',
  },
  cartaRara: {
    backgroundColor: '#fffbe6',
    borderColor: '#FFD700',
  },
  cartaEpica: {
    backgroundColor: '#e0e7ff',
    borderColor: '#7c3aed',
  },
  cartaLendaria: {
    backgroundColor: '#fff0f6',
    borderColor: '#ff1744',
  },
  numeroCarta: {
    fontSize: 48,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 8,
  },
  nomeCarta: {
    fontSize: 28,
    fontFamily: 'Montserrat-ExtraBold',
    color: '#2e7d32',
    marginBottom: 8,
  },
  tipoCarta: {
    fontSize: 18,
    fontFamily: 'Montserrat-Bold',
    marginBottom: 16,
    letterSpacing: 2,
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 8,
    overflow: 'hidden',
  },
  tipoComum: {
    backgroundColor: '#b2dfdb',
    color: '#2e7d32',
  },
  tipoRara: {
    backgroundColor: '#FFD700',
    color: '#7c6500',
  },
  tipoEpica: {
    backgroundColor: '#7c3aed',
    color: '#fff',
  },
  tipoLendaria: {
    backgroundColor: '#ff1744',
    color: '#fff',
  },
  descricao: {
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
    color: '#555',
    textAlign: 'center',
    marginTop: 12,
  },
  naoEncontrada: {
    fontSize: 20,
    color: '#c00',
    fontFamily: 'Montserrat-Bold',
  },
})