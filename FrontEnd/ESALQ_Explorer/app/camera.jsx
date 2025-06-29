import React, { useState, useEffect } from 'react'
import { StyleSheet, Text, View, Button, Alert, TextInput, KeyboardAvoidingView, Platform } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useRouter } from 'expo-router'

const ColetaManual = () => {
  const [input, setInput] = useState('')
  const [nickname, setNickname] = useState('')
  const router = useRouter()

  // Carrega o nickname do usuário ao abrir a tela
  useEffect(() => {
    AsyncStorage.getItem('nickname').then(n => n && setNickname(n))
  }, [])

  const handleColetar = async () => {
    if (!nickname) {
      Alert.alert('Erro', 'Usuário não identificado.')
      return
    }
    const numero = parseInt(input, 10)
    if (isNaN(numero)) {
      Alert.alert('Entrada inválida', 'Digite um número válido.')
      return
    }
    const storageKey = `cartasColetadas_${nickname}`
    const stored = await AsyncStorage.getItem(storageKey)
    let coletadas = stored ? JSON.parse(stored) : []
    if (!coletadas.includes(numero)) {
      coletadas.push(numero)
      await AsyncStorage.setItem(storageKey, JSON.stringify(coletadas))
      Alert.alert('Sucesso', `Carta ${numero} coletada!`)
    } else {
      Alert.alert('Já coletada', `A carta ${numero} já foi coletada.`)
    }
    setInput('')
    setTimeout(() => router.push('/colecao'), 1000)
  }

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={60}
    >
      <View style={styles.container}>
        <Text style={styles.label}>Digite o número da carta coletada:</Text>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          keyboardType="numeric"
          placeholder="Ex: 1"
          maxLength={3}
        />
        <Button title="Coletar carta" onPress={handleColetar} />
      </View>
    </KeyboardAvoidingView>
  )
}

export default ColetaManual

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  label: {
    fontSize: 18,
    marginBottom: 12,
  },
  input: {
    borderWidth: 1,
    borderColor: '#888',
    borderRadius: 8,
    padding: 10,
    width: 100,
    fontSize: 18,
    marginBottom: 16,
    textAlign: 'center',
  },
})