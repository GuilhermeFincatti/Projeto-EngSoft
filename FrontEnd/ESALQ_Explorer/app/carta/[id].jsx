import { View, Text, StyleSheet } from 'react-native'
import { useLocalSearchParams } from 'expo-router'
import { cartas } from './cartas'
import React from 'react'

const TOTAL_CARTAS = 30


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

  return (
    <View style={styles.container}>
      <View style={[
        styles.cartaDetalhe,
        carta.tipo === 'rara' ? styles.cartaRara : styles.cartaComum
      ]}>
        <Text style={styles.numeroCarta}>{carta.id.toString().padStart(2, '0')}</Text>
        <Text style={styles.nomeCarta}>{carta.nome}</Text>
        <Text style={[
          styles.tipoCarta,
          carta.tipo === 'rara' ? styles.tipoRara : styles.tipoComum
        ]}>
          {carta.tipo === 'rara' ? 'RARA' : 'COMUM'}
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
    width: 260,
    height: 340,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    elevation: 4,
    borderWidth: 3,
    marginBottom: 20,
  },
  cartaRara: {
    backgroundColor: '#fffbe6',
    borderColor: '#FFD700',
  },
  cartaComum: {
    backgroundColor: '#e0f2f1',
    borderColor: '#2e7d32',
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
  tipoRara: {
    backgroundColor: '#FFD700',
    color: '#7c6500',
  },
  tipoComum: {
    backgroundColor: '#b2dfdb',
    color: '#2e7d32',
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