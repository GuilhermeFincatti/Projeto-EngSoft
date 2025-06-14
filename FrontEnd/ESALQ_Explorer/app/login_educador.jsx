import { Text, View, StyleSheet, TouchableOpacity, Alert, Pressable } from 'react-native'
import { TextInput, Button, Provider as PaperProvider } from 'react-native-paper'
import { BACKEND_URL } from '../constants/api'
import { useState } from 'react'
import { Link, useRouter } from 'expo-router'
import { ActivityIndicator } from 'react-native'

const login_educador = () => {
  const [nickname, setNickname] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter() // Inicializando o hook para redirecionar após login

  const handleLogin = async () => { // Função para lidar com o login
    // Verifica se os campos estão preenchidos
    if (!nickname || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos.')
      return
    }
    setLoading(true) // Inicia o estado de carregamento

    try {
      const response = await fetch(`${BACKEND_URL}/login`, { // URL do backend
        // Substitua pelo IP do seu backend no arquivo constants/api.js
        // Certifique-se de que o backend está rodando e acessível
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nickname: nickname,
          password: senha,
        }),
      })

      const data = await response.json()
      if (response.ok) { // Caso de sucesso 
        // Alert.alert('Sucesso', 'Login realizado com sucesso!')
        await AsyncStorage.setItem('nickname', nickname) // Armazena o nickname no AsyncStorage
        router.replace('/home') // Redireciona para a home
      } else { // Caso de erro
        // Exibe o erro retornado pelo backend
        console.error('Erro ao fazer login:', data)
        Alert.alert('Erro', JSON.stringify(data));
      }
    } catch (error) { // Captura erros de rede ou outros problemas
      Alert.alert('Erro', 'Não foi possível conectar ao servidor.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PaperProvider>
      <View style={styles.container}>
        <Text style={styles.title}>ESALQ Explorer</Text>
        <Text style={styles.subtitle}>Seja bem-vindo!</Text>
        <Text style={styles.loginText}>Efetue seu Login</Text>

        <TextInput // Componente de entrada de texto para o usuário
          label="Usuário"
          value={nickname}
          onChangeText={setNickname}
          mode="outlined"
          style={styles.input}
          outlineColor="#ccc"
          activeOutlineColor="#2e7d32"
        />

        <TextInput // Componente de entrada de texto para a senha
          label="Senha"
          value={senha}
          onChangeText={setSenha}
          mode="outlined"
          secureTextEntry
          style={styles.input}
          outlineColor="#ccc"
          activeOutlineColor="#2e7d32"
        />

        <Pressable
          style={({ pressed }) => [
            styles.loginButton,
            pressed && { opacity: 0.6 },
            loading && { opacity: 0.5 },
          ]}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator size="small" color="#fff" />
          ) : (
            <Text style={styles.loginButtonText}>Entrar</Text>
          )}
        </Pressable>

        <TouchableOpacity style={styles.googleButton}>
          <Text style={styles.googleButtonText}>Entrar com Google</Text>
        </TouchableOpacity>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Não tem conta? </Text>
        </View>

        <Link href="/registro_educador" asChild>
          <TouchableOpacity style={styles.createAccountButton}>
            <Text style={styles.createAccountButtonText}>Criar uma conta de Educador</Text>
          </TouchableOpacity>
        </Link>

      </View>
    </PaperProvider>
  )
}

export default login_educador

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
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
    marginBottom: 10,
  },
  loginText: {
    fontSize: 20,
    fontFamily: 'Montserrat-Regular',
    fontWeight: '600',
    marginBottom: 20,
    color: '#333',
  },
  input: {
    width: '100%',
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  loginButton: {
    backgroundColor: '#2e7d32',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
    marginBottom: 10,
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  googleButton: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#2e7d32',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
    marginBottom: 20,
  },
  googleButtonText: {
    color: '#2e7d32',
    fontSize: 16,
    fontWeight: '600',
  },
  footer: {
    flexDirection: 'row',
  },
  footerText: {
    color: '#555',
    fontFamily: 'Montserrat-Regular',
  },
  footerLink: {
    color: '#2e7d32',
    fontWeight: '600',
  },
  createAccountButton: {
    backgroundColor: '#e0f2f1',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
    marginBottom: 30,
    borderWidth: 1,
    borderColor: '#2e7d32',
    marginVertical: '20'
  },
  createAccountButtonText: {
    color: '#2e7d32',
    fontSize: 16,
    fontWeight: '600',
  },
})
