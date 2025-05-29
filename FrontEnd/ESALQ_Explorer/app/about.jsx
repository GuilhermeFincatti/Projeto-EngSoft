import { StyleSheet, Text, View, useColorScheme, Pressable } from 'react-native'
import { Link } from 'expo-router'
import { Colors } from "../constants/Colors"
import { useRouter } from 'expo-router'

const about = () => {
  const colorScheme = useColorScheme()
  const theme = Colors[colorScheme] ?? Colors.light
  const router = useRouter()

  return (
    <View style = {[styles.container, { backgroundColor: theme.background }]}>
      <Text style = {styles.title}>
        About page
      </Text>

      <Pressable onPress={() => router.replace('/')}>
        <Text>Back Home</Text>
      </Pressable>
    </View>
  )
}

export default about

const styles = StyleSheet.create({
  container: {
      flex: 1,
      alignItems: 'center',
      justifyContent: 'center'
    },

    title: {
      fontWeight: 'bold',
      fontSize: 18
    },

    link: {
      marginVertical: 10,
      borderBottomWidth: 1
    }
})