import { Stack } from 'expo-router'
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
        <Stack.Screen name="home" options={{ title: 'Mapa', headerBackVisible: false}} />
        <Stack.Screen name="colecao" options={{ title: 'Coleção'}} />
        <Stack.Screen name="missoes" options={{ title: 'Missões'}} />
        <Stack.Screen name="perfil" options={{ title: 'Perfil'}} />
        <Stack.Screen name="leaderboard" options={{ title: 'Ranking'}} />
        <Stack.Screen name="amigos" options={{ title: 'Amigos'}} />
        <Stack.Screen name="carta/[id]" options={{ title: 'Carta'}} />
        <Stack.Screen name="carta/cartas" options={{title: 'json'}}/>
        <Stack.Screen name="camera" options={{ title: 'Scanner QR', headerBackVisible: true }} />
        <Stack.Screen name="test-qr" options={{ title: 'QR Codes de Teste', headerBackVisible: true }} />
      </Stack>
    </>
  )
}

export default RootLayout

const styles = StyleSheet.create({})