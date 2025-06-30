import React, { useEffect, useState } from 'react'
import { StyleSheet, Text, View, Image, TouchableOpacity, Alert, ActivityIndicator, ScrollView } from 'react-native'
import * as ImagePicker from 'expo-image-picker'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { apiService } from '../services/api'
import { useProfileImage } from '../hooks/useProfileImage'

const perfil = () => {
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [uploadingPhoto, setUploadingPhoto] = useState(false)

  // Hook para gerenciar a foto de perfil
  const { profileImage, updateProfileImage, refreshProfileImage } = useProfileImage()

  // Dados do usuário vindos do backend
  const [userData, setUserData] = useState({
    nickname: '',
    ranking: 'Iniciante',
    xp: 0,
    nivel: 1,
    qtdcartas: 0,
    fotoperfil: null
  })

  // Estatísticas da coleção
  const [colecaoStats, setColecaoStats] = useState({
    total_cartas: 0,
    cartas_unicas: 0,
    raridades: {}
  })

  const [missoes, setMissoes] = useState(0)

  useEffect(() => {
    carregarDadosPerfil()
  }, [])

  const carregarDadosPerfil = async () => {
    try {
      setLoading(true)
      setError(null)

      // Carrega dados básicos do AsyncStorage
      const nickname = await AsyncStorage.getItem('nickname')
      const emailStorage = await AsyncStorage.getItem('email')

      if (nickname) setNome(nickname)
      if (emailStorage) setEmail(emailStorage)

      // Busca estatísticas completas do backend
      if (nickname) {
        try {
          const profileStats = await apiService.getProfileStats(nickname)
          console.log('Profile stats carregadas:', profileStats)

          if (profileStats.success) {
            const data = profileStats.data
            setUserData({
              nickname: data.nickname || nickname,
              ranking: data.ranking || 'Iniciante',
              xp: data.xp || 0,
              nivel: data.nivel || 1,
              qtdcartas: data.qtdcartas || 0,
              fotoperfil: data.fotoperfil
            })

            if (data.colecao_stats) {
              setColecaoStats(data.colecao_stats)
            }

            // Atualizar foto de perfil se mudou no backend
            if (data.fotoperfil) {
              await refreshProfileImage()
            }

          } else {
            console.warn('Erro ao carregar stats:', profileStats.error)
          }
        } catch (apiError) {
          console.warn('Erro ao conectar com API:', apiError)
          // Continua com dados do storage local
        }

        // Buscar missões (simulação por enquanto)
        try {
          const missoesData = await apiService.getMissoes()
          const missoesCompletas = missoesData.filter(m => m.concluida).length
          setMissoes(missoesCompletas)
        } catch (missaoError) {
          console.warn('Erro ao carregar missões:', missaoError)
          setMissoes(0)
        }
      }

    } catch (error) {
      console.error('Erro ao carregar dados do perfil:', error)
      setError('Erro ao carregar dados do perfil')
    } finally {
      setLoading(false)
    }
  }

  const pickImage = async () => {
    try {
      let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 0.7,
      })
      
      if (!result.canceled) {
        const imageUri = result.assets[0].uri
        
        // Usar o hook para atualizar a foto de perfil
        if (userData.nickname) {
          try {
            setUploadingPhoto(true)
            console.log('Iniciando upload da foto para:', userData.nickname)
            
            const uploadResult = await updateProfileImage(imageUri)
            console.log('Resultado do upload:', uploadResult)
            
            if (uploadResult.success) {
              Alert.alert('Sucesso', 'Foto de perfil atualizada com sucesso!')
              
              // Recarregar dados do perfil para pegar a nova foto
              await carregarDadosPerfil()
            } else {
              console.error('Upload falhou:', uploadResult)
              Alert.alert('Erro', uploadResult.error || 'Erro ao atualizar foto de perfil')
            }
          } catch (error) {
            console.error('Erro durante upload:', error)
            Alert.alert('Erro', 'Erro inesperado ao atualizar foto de perfil')
          } finally {
            setUploadingPhoto(false)
          }
        } else {
          Alert.alert('Erro', 'Usuário não identificado. Faça login novamente.')
        }
      }
    } catch (error) {
      console.error('Erro ao selecionar imagem:', error)
      Alert.alert('Erro', 'Erro ao selecionar imagem')
    }
  }

  // Função para calcular estatísticas das cartas por raridade
  const getCartasPorRaridade = () => {
    const raridades = colecaoStats.raridades || {}
    return {
      comum: raridades.comum?.unicas || 0,
      incomum: raridades.incomum?.unicas || 0,
      rara: raridades.rara?.unicas || 0,
      épica: raridades.épica?.unicas || 0,
      lendária: raridades.lendária?.unicas || 0,
      total: colecaoStats.cartas_unicas || userData.qtdcartas || 0
    }
  }

  if (loading && !uploadingPhoto) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color="#2e7d32" />
        <Text style={styles.loadingText}>Carregando perfil...</Text>
      </View>
    )
  }

  if (error) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={carregarDadosPerfil}>
          <Text style={styles.retryButtonText}>Tentar Novamente</Text>
        </TouchableOpacity>
      </View>
    )
  }

  const cartasStats = getCartasPorRaridade()

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      <TouchableOpacity 
        onPress={pickImage} 
        style={styles.profileImageContainer}
        disabled={uploadingPhoto}
      >
        <Image
          source={
            profileImage
              ? { uri: profileImage }
              : require('../assets/perfil.png')
          }
          style={styles.profileImage}
        />
        {uploadingPhoto && (
          <View style={styles.uploadOverlay}>
            <ActivityIndicator size="small" color="#fff" />
          </View>
        )}
        <Text style={styles.editPhoto}>
          {uploadingPhoto ? 'Enviando...' : 'Editar foto'}
        </Text>
      </TouchableOpacity>

      <Text style={styles.nome}>{userData.nickname || nome || 'Seu Nome'}</Text>
      
      {/* Informações de XP e Nível */}
      <View style={styles.xpSection}>
        <Text style={styles.xpText}>XP: {userData.xp}</Text>
        <Text style={styles.nivelText}>Nível {userData.nivel}</Text>
        <Text style={styles.rankingText}>{userData.ranking}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Cartas Coletadas</Text>
        <View style={styles.cartasRow}>
          <View style={[styles.cartaBox, styles.comum]}>
            <Text style={styles.cartaQtd}>{cartasStats.comum}</Text>
            <Text style={styles.cartaTipo}>Comum</Text>
          </View>
          <View style={[styles.cartaBox, styles.incomum]}>
            <Text style={styles.cartaQtd}>{cartasStats.incomum}</Text>
            <Text style={styles.cartaTipo}>Incomum</Text>
          </View>
          <View style={[styles.cartaBox, styles.rara]}>
            <Text style={styles.cartaQtd}>{cartasStats.rara}</Text>
            <Text style={styles.cartaTipo}>Rara</Text>
          </View>
          <View style={[styles.cartaBox, styles.epica]}>
            <Text style={styles.cartaQtd}>{cartasStats.épica}</Text>
            <Text style={styles.cartaTipo}>Épica</Text>
          </View>
          <View style={[styles.cartaBox, styles.lendaria]}>
            <Text style={styles.cartaQtd}>{cartasStats.lendária}</Text>
            <Text style={styles.cartaTipo}>Lendária</Text>
          </View>
        </View>
        <Text style={styles.totalCartas}>Total: {cartasStats.total}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Missões Completas</Text>
        <Text style={styles.missoesQtd}>{missoes}</Text>
      </View>
    </ScrollView>
  )
}

export default perfil

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#e0f2f1',
  },
  contentContainer: {
    alignItems: 'center',
    paddingTop: 40,
    paddingHorizontal: 20,
    paddingBottom: 30,
  },
  profileImageContainer: {
    alignItems: 'center',
    marginBottom: 16,
    position: 'relative',
  },
  profileImage: {
    width: 110,
    height: 110,
    borderRadius: 55,
    borderWidth: 3,
    borderColor: '#2e7d32',
    backgroundColor: '#fff',
  },
  uploadOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 25,
    backgroundColor: 'rgba(0,0,0,0.5)',
    borderRadius: 55,
    justifyContent: 'center',
    alignItems: 'center',
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
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#2e7d32',
    fontFamily: 'Montserrat-Regular',
    marginTop: 10,
  },
  errorText: {
    fontSize: 16,
    color: '#d32f2f',
    fontFamily: 'Montserrat-Regular',
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#2e7d32',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontFamily: 'Montserrat-Bold',
  },
  xpSection: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 18,
    marginBottom: 18,
    alignItems: 'center',
    elevation: 2,
    width: '100%',
  },
  xpText: {
    fontSize: 24,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 4,
  },
  nivelText: {
    fontSize: 20,
    fontFamily: 'Montserrat-Bold',
    color: '#4caf50',
    marginBottom: 4,
  },
  rankingText: {
    fontSize: 18,
    fontFamily: 'Montserrat-Bold',
    color: '#ff9800',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  incomum: { 
    backgroundColor: '#f0fff0',
    borderColor: '#32CD32',
    borderWidth: 1,
  },
})