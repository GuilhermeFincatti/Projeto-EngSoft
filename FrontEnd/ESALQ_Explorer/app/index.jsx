import { StyleSheet, Text, View, Pressable} from 'react-native'
import { Link } from 'expo-router'

const Home = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>ESALQ Explorer</Text>
      <Text style={styles.subtitle}>Seja bem-vindo!</Text>

      <View style={styles.buttonContainer}>
        <Link href="/login_explorador" asChild>
          <Pressable style={styles.button}>
            <Text style={styles.buttonText}>Entre como Explorador</Text>
          </Pressable>
        </Link>

        <Link href="/login_educador" asChild>
          <Pressable style={styles.button}>
            <Text style={styles.buttonText}>Entre como Educador</Text>
          </Pressable>
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
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2e7d32',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 22,
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
