import { Stack, Tabs } from 'expo-router'
import { StyleSheet, useColorScheme } from 'react-native'
import { Colors } from "../constants/Colors"
import { StatusBar } from 'expo-status-bar'
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';

const RootLayout = () => {
  const colorScheme = useColorScheme()
  const theme = Colors[colorScheme] ?? Colors.light
  const [fontsLoaded, fontError] = useFonts({
    'Montserrat-Regular': require('../assets/fonts/Montserrat-Regular.ttf'),
    'Montserrat-Bold': require('../assets/fonts/Montserrat-Bold.ttf'),
    'Montserrat-ExtraBold': require('../assets/fonts/Montserrat-ExtraBold.ttf'),
  });

  useEffect(() => {
    // Agora este bloco tem 100% de controle sobre quando a splash screen some.
    if (fontsLoaded || fontError) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded, fontError]);

  if (!fontsLoaded && !fontError) {
    return null;
  }

  return (
    <>
      <StatusBar style={colorScheme === 'dark' ? 'light' : 'dark'}/>
      <Stack screenOptions={{ 
        headerStyle: { backgroundColor: theme.navBackground}, 
        headerTintColor: theme.title, 
      }}>
        <Stack.Screen name="index" options={{ title: 'Home', headerBackVisible: false , headerShown: false}}/>
        <Stack.Screen name="login_educador" options={{ title: 'Login Educador' }}/>
        <Stack.Screen name="login_explorador" options={{ title: 'Login Explorador' }}/>
        <Stack.Screen name="registro_educador" options={{ title: 'Crie sua conta' }}/>
        <Stack.Screen name="registro_explorador" options={{ title: 'Crie sua conta' }}/>
        <Stack.Screen name="tabs" options={{ headerShown: false }} />
      </Stack>
    </>
  )
}

export default RootLayout

const styles = StyleSheet.create({})