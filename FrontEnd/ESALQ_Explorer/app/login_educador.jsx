import { Text, View, StyleSheet, TouchableOpacity, Alert } from 'react-native'
import { TextInput, Button, Provider as PaperProvider } from 'react-native-paper'
import { useState } from 'react'
import { Link, useRouter } from 'expo-router' // Adicione useRouter

const login_educador = () => {
  const [nickname, setNickname] = useState('')
  const [senha, setSenha] = useState('')
  const router = useRouter() // Inicialize o hook

  const handleLogin = async () => {
    if (!nickname || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos.')
      return
    }

    try {
      const response = await fetch('http://192.168.145.63:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nickname: nickname,
          password: senha,
        }),
      })

      const data = await response.json()
      if (response.ok) {
        // Alert.alert('Sucesso', 'Login realizado com sucesso!')
        router.replace('/home') // Redireciona para a home
      } else {
        Alert.alert('Erro', JSON.stringify(data));
      }
    } catch (error) {
      Alert.alert('Erro', 'Não foi possível conectar ao servidor.')
    }
  }

  return (
    <PaperProvider>
      <View style={styles.container}>
        <Text style={styles.title}>ESALQ Explorer</Text>
        <Text style={styles.subtitle}>Seja bem-vindo!</Text>
        <Text style={styles.loginText}>Efetue seu Login</Text>

        <TextInput
          label="Usuário"
          value={nickname}
          onChangeText={setNickname}
          mode="outlined"
          style={styles.input}
          outlineColor="#ccc"
          activeOutlineColor="#2e7d32"
        />

        <TextInput
          label="Senha"
          value={senha}
          onChangeText={setSenha}
          mode="outlined"
          secureTextEntry
          style={styles.input}
          outlineColor="#ccc"
          activeOutlineColor="#2e7d32"
        />

        <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
          <Text style={styles.loginButtonText}>Entrar</Text>
        </TouchableOpacity>

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
