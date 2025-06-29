import React, { useState, useEffect } from 'react'
import { View, Text, TouchableOpacity, Alert, StyleSheet } from 'react-native'
import { apiService, ApiError, NetworkError } from '../services/api'

const CartaCollectButton = ({ cartaId, onCartaColetada }) => {
  const [loading, setLoading] = useState(false)

  const adicionarCarta = async () => {
    try {
      setLoading(true)
      await apiService.adicionarCartaColecao(cartaId)
      Alert.alert('Sucesso!', 'Carta adicionada à sua coleção!')
      if (onCartaColetada) {
        onCartaColetada(cartaId)
      }
    } catch (error) {
      console.error('Erro ao adicionar carta:', error)
      
      let errorMessage = 'Erro ao adicionar carta à coleção.'
      
      if (error instanceof ApiError) {
        errorMessage = error.getUserMessage()
      } else if (error instanceof NetworkError) {
        errorMessage = error.getUserMessage()
      }
      
      Alert.alert('Erro', errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <TouchableOpacity 
      style={[styles.button, loading && styles.buttonDisabled]} 
      onPress={adicionarCarta}
      disabled={loading}
    >
      <Text style={styles.buttonText}>
        {loading ? 'Coletando...' : 'Coletar Carta'}
      </Text>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#2e7d32',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
})

export default CartaCollectButton
