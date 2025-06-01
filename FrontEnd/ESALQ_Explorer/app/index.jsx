import { StyleSheet, Text, View, TouchableOpacity, Image} from 'react-native'
import { Link } from 'expo-router'

const Home = () => {
  return (
    <View style={styles.container}>
      <Image
        source={require('../assets/Logo_ESALQ_Explorer_Sem_Texto.png')} // Substitua pelo caminho correto da sua imagem
        style={styles.logo}
        resizeMode="center" // Ou 'cover', 'stretch', 'repeat', 'center'
      />

      <Image
        source={require('../assets/Logo_ESALQ_Explorer_Texto.png')} // Substitua pelo caminho correto da sua imagem
        style={styles.textoLogo}
        resizeMode="center" // Ou 'cover', 'stretch', 'repeat', 'center'
      /> 

      <Text style={styles.subtitle}>Seja bem-vindo!</Text>

      <View style={styles.buttonContainer}>
        <Link href="/login_explorador" asChild>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Entre como Explorador</Text>
          </TouchableOpacity>
        </Link>

        <Link href="/login_educador" asChild>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Entre como Educador</Text>
          </TouchableOpacity>
        </Link>
      </View>
    </View>
  )
}

export default Home

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  logo: {
    width: 200, 
    height: 150,
    transform: [
      { translateX: 5 } // Move a imagem 15 pixels para a ESQUERDA.
    ],
  },
  textoLogo: {
    width: 150,
    height: 70,
    marginBottom: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 22,
    fontFamily: 'Montserrat-Bold',
    color: '#63a355',
    marginBottom: 40,
  },
  buttonContainer: {
    width: '100%',
    gap: 20,
  },
  button: {
    backgroundColor: '#2e7d32',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
})
