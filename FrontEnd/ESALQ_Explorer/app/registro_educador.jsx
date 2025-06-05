import React, { useState } from 'react'
import { StyleSheet, Text, TextInput, View, Pressable, Alert, ScrollView, KeyboardAvoidingView, Platform } from 'react-native'
import { BACKEND_URL } from '../constants/api'
import { useRouter } from 'expo-router'

const registro_educador = () => {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter() // Inicializando o hook para redirecionar após o registro

  const handleRegister = async () => { // Função para lidar com o registro
    // Verifica se os campos estão preenchidos
    if (!username || !email || !password) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos.')
      return
    }

    try { 
      const response = await fetch(`${BACKEND_URL}/register`, { // URL do backend
        // Substitua pelo IP do seu backend
        // Certifique-se de que o backend está rodando e acessível
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nickname: username,
          email: email,
          password: password,
          tipo: 'educador' // ou 'educador' dependendo do cadastro
        }),
      })

      const data = await response.json()

      if (response.ok) { // Caso de sucesso
        Alert.alert('Sucesso', 'Registro concluído com sucesso!')
        console.log('Dados do usuário:', data)
        router.push('/login_educador') // Redireciona para a página de login do educador
      } else { // Caso de erro
        console.error('Erro no registro:', data)
        Alert.alert('Erro no registro. Tente novamente mais tarde.')
      }
    } catch (error) { // Captura erros de rede ou outros problemas
      console.error('Erro na requisição:', error)
      Alert.alert('Erro', 'Não foi possível conectar ao servidor.')
    }
  }

  return (
    <KeyboardAvoidingView // Componente para evitar que o teclado cubra os campos de entrada
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 60 : 0} // Ajuste se necessário
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>ESALQ Explorer</Text>
        <Text style={styles.loginText}>Crie sua conta de Educador</Text>

        <TextInput // Componente de entrada de texto para o nome de usuário
          style={styles.input}
          placeholder="Nome de usuário"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
          autoCorrect={false}
        />

        <TextInput // Componente de entrada de texto para o e-mail
          style={styles.input}
          placeholder="E-mail"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />

        <TextInput // Componente de entrada de texto para a senha
          style={styles.input}
          placeholder="Senha"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Pressable
          style={({ pressed }) => [
            styles.registerButton,
            pressed && { opacity: 0.6 }, // Efeito de opacidade quando pressionado
          ]}
          onPress={handleRegister}
        >
          <Text style={styles.registerButtonText}>Registrar</Text>
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  )
}

export default registro_educador

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    paddingVertical: 40,
  },
  title: {
    fontSize: 28,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 4,
  },
  loginText: {
    fontSize: 20,
    fontFamily: 'Montserrat-Regular',
    fontWeight: '600',
    marginBottom: 30,
    color: '#333',
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 20,
    backgroundColor: '#f9f9f9',
  },
  registerButton: {
    backgroundColor: '#2e7d32',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
    marginTop: 10,
  },
  registerButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
})