import { StyleSheet, Text, View, FlatList, TouchableOpacity, ScrollView } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useRouter } from 'expo-router'
import { cartas } from './carta/cartas'
import AsyncStorage from '@react-native-async-storage/async-storage'


const colecao = () => {
  const [cartasColetadas, setCartasColetadas] = useState([])
  const [nickname, setNickname] = useState('')
  const router = useRouter()

  useEffect(() => {
    // Busca o nickname e depois as cartas coletadas desse usuário
    AsyncStorage.getItem('nickname').then(nick => {
      if (nick) {
        setNickname(nick)
        const storageKey = `cartasColetadas_${nick}`
        AsyncStorage.getItem(storageKey).then(data => {
          setCartasColetadas(data ? JSON.parse(data) : [])
        })
      }
    })
  }, [])

  // Ordena as cartas por id
  const cartasOrdenadas = [...cartas].sort((a, b) => a.id - b.id)

  const renderCarta = ({ item }) => {
    const coletada = cartasColetadas.includes(item.id)
    return (
      <TouchableOpacity
        style={[
          styles.carta,
          styles[`carta_${item.tipo}`],
          coletada && styles.cartaColetada,
        ]}
        onPress={coletada ? () => router.push(`/carta/${item.id}`) : undefined}
        activeOpacity={coletada ? 0.7 : 1}
      >
        <Text style={[styles.numeroCarta, coletada && styles.numeroCartaColetada]}>
          {item.id.toString().padStart(2, '0')}
        </Text>
        <Text style={styles.statusCarta}>
          {coletada ? item.tipo.charAt(0).toUpperCase() + item.tipo.slice(1) : '???'}
        </Text>
      </TouchableOpacity>
    )
  }

  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.container}>
        <Text style={styles.title}>Coleção de Cartas</Text>
        <Text style={styles.subtitle}>Complete sua coleção!</Text>
        <FlatList
          data={cartasOrdenadas}
          renderItem={renderCarta}
          keyExtractor={item => item.id.toString()}
          numColumns={3}
          contentContainerStyle={styles.grid}
          scrollEnabled={false}
        />
      </View>
    </ScrollView>
  )
}

export default colecao

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#transparent',
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
  scrollContainer: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingBottom: 40,
  },
  grid: {
    alignItems: 'center',
    paddingBottom: 10,
  },
  carta: {
    borderWidth: 2,
    borderRadius: 16,
    width: 90,
    height: 120,
    margin: 10,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 2,
    backgroundColor: '#e0f2f1',
    borderColor: '#2e7d32',
  },
  cartaColetada: {
    opacity: 1,
  },
  carta_comum: {
    backgroundColor: '#e0f2f1',
    borderColor: '#2e7d32',
  },
  carta_rara: {
    backgroundColor: '#fffbe6',
    borderColor: '#FFD700',
  },
  carta_épica: {
    backgroundColor: '#e0e7ff',
    borderColor: '#7c3aed',
  },
  carta_lendária: {
    backgroundColor: '#fff0f6',
    borderColor: '#ff1744',
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