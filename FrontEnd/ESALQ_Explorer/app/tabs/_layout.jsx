import { Tabs } from 'expo-router'
import { StyleSheet, useColorScheme } from 'react-native'
import { Colors } from "../../constants/Colors"
import { StatusBar } from 'expo-status-bar'
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';

const RootLayout = () => {
  const colorScheme = useColorScheme()
  const theme = Colors[colorScheme] ?? Colors.light
  const [fontsLoaded, fontError] = useFonts({
    'Montserrat-Regular': require('../../assets/fonts/Montserrat-Regular.ttf'),
    'Montserrat-Bold': require('../../assets/fonts/Montserrat-Bold.ttf'),
    'Montserrat-ExtraBold': require('../../assets/fonts/Montserrat-ExtraBold.ttf'),
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
      <Tabs
        screenOptions={{
          headerStyle: { backgroundColor: theme.navBackground },
          headerTintColor: theme.title,
        }}
      >
        <Tabs.Screen name="home" options={{ title: 'Mapa', headerShown: false }} />
        <Tabs.Screen name="colecao" options={{ title: 'Coleção' }} />
        <Tabs.Screen name="camera" options={{ title: 'QR Code' }} />
        <Tabs.Screen name="missoes" options={{ title: 'Missões' }} />
        <Tabs.Screen name="perfil" options={{ title: 'Perfil' }} />
      </Tabs>
    </>
  )
}

export default RootLayout

const styles = StyleSheet.create({})