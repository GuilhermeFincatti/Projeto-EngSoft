import { StyleSheet, Text, View, FlatList, TouchableOpacity } from 'react-native'
import React from 'react'

const TOTAL_CARTAS = 30 // Altere conforme necessário

const colecao = () => {
  // Precisa integrar com Backend para obter as cartas coletadas
  const cartasColetadas = [1, 2, 5, 7, 10, 12, 15]

  const renderCarta = ({ item }) => {
    const coletada = cartasColetadas.includes(item)
    return (
      <TouchableOpacity style={[styles.carta, coletada && styles.cartaColetada]}>
        <Text style={[styles.numeroCarta, coletada && styles.numeroCartaColetada]}>
          {item.toString().padStart(2, '0')}
        </Text>
        <Text style={styles.statusCarta}>
          {coletada ? 'Coletada' : '???'}
        </Text>
      </TouchableOpacity>
    )
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Coleção de Cartas</Text>
      <Text style={styles.subtitle}>Complete sua coleção!</Text>
      <FlatList
        data={Array.from({ length: TOTAL_CARTAS }, (_, i) => i + 1)}
        renderItem={renderCarta}
        keyExtractor={item => item.toString()}
        numColumns={3}
        contentContainerStyle={styles.grid}
        showsVerticalScrollIndicator={false}
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
    height: 120,
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
  },
  cartaColetada: {
    backgroundColor: '#2e7d32',
    borderColor: '#388e3c',
  },
  numeroCarta: {
    fontSize: 32,
    color: '#2e7d32',
    fontFamily: 'Montserrat-Bold',
    marginBottom: 8,
  },
  numeroCartaColetada: {
    color: '#fff',
  },
  statusCarta: {
    fontSize: 14,
    color: '#555',
    fontFamily: 'Montserrat-Regular',
  },
})