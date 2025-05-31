import { Text, View, StyleSheet, TouchableOpacity } from 'react-native'
import { TextInput, Button, Provider as PaperProvider } from 'react-native-paper'
import { useState } from 'react'
import { Link } from 'expo-router'

const login_explorador = () => {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')

  return (
    <PaperProvider>
      <View style={styles.container}>
        <Text style={styles.title}>ESALQ Explorer</Text>
        <Text style={styles.subtitle}>Seja bem-vindo!</Text>
        <Text style={styles.loginText}>Efetue seu Login</Text>

        <TextInput
          label="E-mail"
          value={email}
          onChangeText={setEmail}
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

        <TouchableOpacity style={styles.loginButton}>
          <Text style={styles.loginButtonText}>Entrar</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.googleButton}>
          <Text style={styles.googleButtonText}>Entrar com Google</Text>
        </TouchableOpacity>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Não tem conta? </Text>
        </View>

        <Link href="/registro_explorador" asChild>
          <TouchableOpacity style={styles.createAccountButton}>
            <Text style={styles.createAccountButtonText}>Criar uma conta de Explorador</Text>
          </TouchableOpacity>
        </Link>

      </View>
    </PaperProvider>
  )
}

export default login_explorador

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
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 18,
    color: '#555',
    marginBottom: 10,
  },
  loginText: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 20,
    color: '#333',
  },
  input: {
    width: '100%',
    marginBottom: 15,
    backgroundColor: '#fff', // Importante para não ficar cinza
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
  },
  footerLink: {
    color: '#2e7d32',
    fontWeight: '600',
  },
  createAccountButton: {
    backgroundColor: '#e0f2f1', // Verde claro para destacar, mas suave
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
