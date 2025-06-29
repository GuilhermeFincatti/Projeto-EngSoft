import { Text, View, StyleSheet, TouchableOpacity, Alert, Pressable } from 'react-native'
import { TextInput, Button, Provider as PaperProvider } from 'react-native-paper'
import { useState } from 'react'
import { Link, useRouter } from 'expo-router'
import { ActivityIndicator } from 'react-native'
import { apiService, ApiError, NetworkError } from '../services/api'

const login_educador = () => {
  const [nickname, setNickname] = useState('')
  const [senha, setSenha] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter() // Inicializando o hook para redirecionar após login

  const handleLogin = async () => { 
    // Verifica se os campos estão preenchidos
    if (!nickname || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos.')
      return
    }
    setLoading(true)

    try {
      await apiService.login(nickname, senha)
      // Login bem-sucedido - redireciona para home
      router.replace('/home')
    } catch (error) {
      console.error('Erro ao fazer login:', error)
      
      let errorMessage = 'Erro desconhecido. Tente novamente.'
      
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
