import { useState, useEffect } from 'react'
import { apiService } from '../services/api'
import AsyncStorage from '@react-native-async-storage/async-storage'

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('access_token')
      const nickname = await AsyncStorage.getItem('nickname')
      
      if (token && nickname) {
        // Verifica se o token ainda é válido
        const isValid = await apiService.validateToken()
        if (isValid) {
          setIsAuthenticated(true)
          setUser({ nickname })
        } else {
          // Token inválido, limpa dados
          await logout()
        }
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error)
      await logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (nickname, password) => {
    try {
      const data = await apiService.login(nickname, password)
      setIsAuthenticated(true)
      setUser({ nickname })
      return data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await apiService.logout()
      setIsAuthenticated(false)
      setUser(null)
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
    }
  }

  const refreshAuth = () => {
    checkAuthStatus()
  }

  return {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    refreshAuth
  }
}
