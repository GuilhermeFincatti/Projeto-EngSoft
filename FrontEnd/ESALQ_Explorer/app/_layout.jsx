import { Stack } from 'expo-router'
import { StyleSheet, Text, useColorScheme, View } from 'react-native'
import { Colors } from "../constants/Colors"
import { StatusBar } from 'expo-status-bar'

const RootLayout = () => {
  const colorScheme = useColorScheme()
  const theme = Colors[colorScheme] ?? Colors.light

  return (
    <>
      <StatusBar style={colorScheme === 'dark' ? 'light' : 'dark'}/>
      <Stack screenOptions = {{ 
        headerStyle: { backgroundColor: theme.navBackground}, 
        headerTintColor: theme.title, 
      }}>
        <Stack.Screen name = "index" options = {{ title: 'Home', headerBackVisible: false , headerShown: false}}/>
        <Stack.Screen name = "login_educador" options = {{ title: 'Login Educador' }}/>
        <Stack.Screen name = "login_explorador" options = {{ title: 'Login Explorador' }}/>
        <Stack.Screen name = "registro_educador" options = {{ title: 'Crie sua conta' }}/>
        <Stack.Screen name = "registro_explorador" options = {{ title: 'Crie sua conta' }}/>
      </Stack>
    </>
    
  )
}

export default RootLayout

const styles = StyleSheet.create({})