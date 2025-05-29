import { StyleSheet, Text, View, Pressable } from 'react-native'
import { Link } from 'expo-router' 
import { useRouter } from 'expo-router'

const contact = () => {
  const colorScheme = useColorScheme()
  const theme = Colors[colorScheme] ?? Colors.light
  const router = useRouter()

  return (
    <View style = {styles.container}>
      <Text style = {styles.title}>
        Contact Page
      </Text>

      <Pressable onPress={() => router.replace('/')}>
        <Text>Back Home</Text>
      </Pressable>
    </View>
  )
}

export default contact

const styles = StyleSheet.create({
    container: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center'
    },

    title: {
      fontWeight: 'bold',
      fontSize: 18
    }
})