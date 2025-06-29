import React, { useEffect, useState } from 'react'
import { StyleSheet, Text, View, Image, TouchableOpacity, Alert } from 'react-native'
import * as ImagePicker from 'expo-image-picker'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useRouter } from 'expo-router'

const perfil = () => {
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [profileImage, setProfileImage] = useState(null)

  // Simulação de dados (substitua por dados do backend futuramente)
  const [cartas, setCartas] = useState({
    total: 18,
    comum: 10,
    rara: 5,
    epica: 2,
    lendaria: 1,
  })
  const [missoes, setMissoes] = useState(7)
  const router = useRouter()

  useEffect(() => {
    // Carrega nome e e-mail do AsyncStorage
    AsyncStorage.getItem('nickname').then(n => n && setNome(n))
    AsyncStorage.getItem('email').then(e => e && setEmail(e))
    AsyncStorage.getItem('profileImage').then(img => img && setProfileImage(img))
    // Aqui você pode buscar as cartas/missões do backend e atualizar os states acima
  }, [])

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [1, 1],
      quality: 0.7,
    })
    if (!result.canceled) {
      setProfileImage(result.assets[0].uri)
      await AsyncStorage.setItem('profileImage', result.assets[0].uri)
    }
  }

  const handleLogout = async () => {
    await AsyncStorage.removeItem('nickname')
    await AsyncStorage.removeItem('email')
    await AsyncStorage.removeItem('profileImage')
    router.replace('/') // ou router.push('/') para voltar para a tela inicial
  }

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={pickImage} style={styles.profileImageContainer}>
        <Image
          source={
            profileImage
              ? { uri: profileImage }
              : require('../assets/perfil.png')
          }
          style={styles.profileImage}
        />
        <Text style={styles.editPhoto}>Editar foto</Text>
      </TouchableOpacity>

      <Text style={styles.nome}>{nome || 'Seu Nome'}</Text>
      

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Cartas Coletadas</Text>
        <View style={styles.cartasRow}>
          <View style={[styles.cartaBox, styles.comum]}>
            <Text style={styles.cartaQtd}>{cartas.comum}</Text>
            <Text style={styles.cartaTipo}>Comum</Text>
          </View>
          <View style={[styles.cartaBox, styles.rara]}>
            <Text style={styles.cartaQtd}>{cartas.rara}</Text>
            <Text style={styles.cartaTipo}>Rara</Text>
          </View>
          <View style={[styles.cartaBox, styles.epica]}>
            <Text style={styles.cartaQtd}>{cartas.epica}</Text>
            <Text style={styles.cartaTipo}>Épica</Text>
          </View>
          <View style={[styles.cartaBox, styles.lendaria]}>
            <Text style={styles.cartaQtd}>{cartas.lendaria}</Text>
            <Text style={styles.cartaTipo}>Lendária</Text>
          </View>
        </View>
        <Text style={styles.totalCartas}>Total: {cartas.total}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Missões Completas</Text>
        <Text style={styles.missoesQtd}>{missoes}</Text>
      </View>

      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Sair</Text>
      </TouchableOpacity>
    </View>
  )
}

export default perfil

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e0f2f1',
    alignItems: 'center',
    paddingTop: 40,
    paddingHorizontal: 20,
  },
  profileImageContainer: {
    alignItems: 'center',
    marginBottom: 16,
  },
  profileImage: {
    width: 110,
    height: 110,
    borderRadius: 55,
    borderWidth: 3,
    borderColor: '#2e7d32',
    backgroundColor: '#fff',
  },
  editPhoto: {
    color: '#2e7d32',
    fontSize: 14,
    marginTop: 6,
    fontFamily: 'Montserrat-Regular',
  },
  nome: {
    fontSize: 28,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginTop: 8,
    marginBottom: 20,
  },
  email: {
    fontSize: 16,
    color: '#555',
    fontFamily: 'Montserrat-Regular',
    marginBottom: 18,
  },
  section: {
    width: '100%',
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 18,
    marginBottom: 18,
    alignItems: 'center',
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 20,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 10,
  },
  cartasRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginBottom: 8,
  },
  cartaBox: {
    flex: 1,
    alignItems: 'center',
    padding: 8,
    marginHorizontal: 4,
    borderRadius: 10,
    backgroundColor: '#e0f2f1',
  },
  comum: { backgroundColor: '#e0f2f1' },
  rara: { backgroundColor: '#fffbe6' },
  epica: { backgroundColor: '#e1bee7' },
  lendaria: { backgroundColor: '#ffd6e0' },
  cartaQtd: {
    fontSize: 22,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
  },
  cartaTipo: {
    fontSize: 14,
    fontFamily: 'Montserrat-Regular',
    color: '#555',
  },
  totalCartas: {
    fontSize: 16,
    color: '#2e7d32',
    fontFamily: 'Montserrat-Bold',
    marginTop: 4,
  },
  missoesQtd: {
    fontSize: 32,
    color: '#2e7d32',
    fontFamily: 'Montserrat-Bold',
    marginTop: 8,
  },
  logoutButton: {
    marginTop: 16,
    backgroundColor: '#ff1744',
    paddingVertical: 10,
    paddingHorizontal: 32,
    borderRadius: 8,
    alignItems: 'center',
  },
  logoutText: {
    color: '#fff',
    fontSize: 18,
    fontFamily: 'Montserrat-Bold',
  },
})