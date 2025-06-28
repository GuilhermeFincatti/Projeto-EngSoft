import { StyleSheet, Text, View, FlatList, TouchableOpacity } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useRouter } from 'expo-router'
import { cartas } from './carta/cartas' // Importa o array correto
import AsyncStorage from '@react-native-async-storage/async-storage'

const colecao = () => {
  const [cartasColetadas, setCartasColetadas] = useState([])
  const router = useRouter()

  useEffect(() => {
    AsyncStorage.getItem('cartasColetadas').then(data => {
      setCartasColetadas(data ? JSON.parse(data) : [])
    })
  }, [])

  const renderCarta = ({ item }) => {
    const coletada = cartasColetadas.includes(item.id)
    return (
      <TouchableOpacity
        style={[
          styles.carta,
          coletada && styles.cartaColetada,
          item.tipo === 'rara' && styles.cartaRara,
        ]}
        onPress={coletada ? () => router.push(`/carta/${item.id}`) : undefined}
        activeOpacity={coletada ? 0.7 : 1}
      >
        <Text style={[styles.numeroCarta, coletada && styles.numeroCartaColetada]}>
          {item.id.toString().padStart(2, '0')}
        </Text>
        <Text style={styles.statusCarta}>
          {coletada ? (item.tipo === 'rara' ? 'Rara' : 'Comum') : '???'}
        </Text>
      </TouchableOpacity>
    )
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Coleção de Cartas</Text>
      <Text style={styles.subtitle}>Complete sua coleção!</Text>
      <FlatList
        data={cartas}
        renderItem={renderCarta}
        keyExtractor={item => item.id.toString()}
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
  cartaRara: {
    borderWidth: 3,
    borderColor: '#FFD700', // Dourado para raras
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