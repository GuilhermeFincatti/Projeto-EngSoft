import { StyleSheet, Text, View, FlatList, TouchableOpacity, ActivityIndicator, RefreshControl, Alert } from 'react-native'
import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'

const missoes = () => {
  const [missoes, setMissoes] = useState([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    carregarMissoes()
  }, [])

  const carregarMissoes = async () => {
    try {
      setLoading(true)
      
      // Buscar missões com progresso calculado
      const missoesComProgresso = await apiService.calcularProgressoMissoes()
      
      // Validar se o resultado é um array
      const missoesValidas = Array.isArray(missoesComProgresso) ? missoesComProgresso : []
      
      // Adicionar algumas missões de exemplo se não houver nenhuma
      if (missoesValidas.length === 0) {
        const missoesExemplo = [
          {
            codigo: 1,
            tipo: 'Coletor Iniciante',
            educador: 'Sistema',
            datainicio: new Date(),
            datafim: null,
            progresso: 3,
            meta: 5,
            tipo: 'quantidade',
            concluida: false,
            porcentagem: 60,
            descricao: 'Colete suas primeiras 5 cartas',
            recompensa: '50 XP',
            icone: '🌱'
          },
          {
            codigo: 2,
            tipo: 'Caçador de Raras',
            educador: 'Sistema',
            datainicio: new Date(),
            datafim: null,
            progresso: 1,
            meta: 3,
            tipo: 'raridade',
            concluida: false,
            porcentagem: 33,
            descricao: 'Encontre 3 cartas raras',
            recompensa: '100 XP',
            icone: '⭐'
          },
          {
            codigo: 3,
            tipo: 'Explorador',
            educador: 'Sistema',
            datainicio: new Date(),
            datafim: null,
            progresso: 7,
            meta: 10,
            tipo: 'quantidade',
            concluida: false,
            porcentagem: 70,
            descricao: 'Colete 10 cartas diferentes',
            recompensa: 'Carta Especial',
            icone: '🗺️'
          },
          {
            codigo: 4,
            tipo: 'Lenda Viva',
            educador: 'Sistema',
            datainicio: new Date(),
            datafim: null,
            progresso: 0,
            meta: 1,
            tipo: 'raridade',
            concluida: false,
            porcentagem: 0,
            descricao: 'Encontre uma carta lendária',
            recompensa: '500 XP + Título',
            icone: '👑'
          },
          {
            codigo: 5,
            tipo: 'Veterano',
            educador: 'Sistema',
            datainicio: new Date(),
            datafim: null,
            progresso: 12,
            meta: 20,
            tipo: 'quantidade',
            concluida: false,
            porcentagem: 60,
            descricao: 'Colete 20 cartas no total',
            recompensa: 'Deck Especial',
            icone: '🏆'
          }
        ]
        setMissoes(missoesExemplo)
      } else {
        setMissoes(missoesValidas)
      }
      
    } catch (error) {
      console.error('Erro ao carregar missões:', error)
      Alert.alert('Erro', 'Não foi possível carregar as missões')
    } finally {
      setLoading(false)
    }
  }

  const onRefresh = async () => {
    setRefreshing(true)
    await carregarMissoes()
    setRefreshing(false)
  }

  const getMissaoStyle = (missao) => {
    const baseStyle = [styles.missaoCard]
    
    if (missao.concluida) {
      baseStyle.push(styles.missaoConcluida)
    } else if (missao.porcentagem >= 80) {
      baseStyle.push(styles.missaoQuaseConcluida)
    }
    
    return baseStyle
  }

  const getProgressBarStyle = (porcentagem) => {
    return {
      ...styles.progressoFill,
      width: `${porcentagem}%`,
      backgroundColor: porcentagem === 100 ? '#4CAF50' : porcentagem >= 80 ? '#FF9800' : '#2e7d32'
    }
  }

  const formatarTipo = (tipo) => {
    switch (tipo) {
      case 'quantidade':
        return 'Coleta'
      case 'raridade':
        return 'Raridade'
      case 'evento':
        return 'Evento'
      default:
        return 'Geral'
    }
  }

  const renderMissao = ({ item }) => {
    // Proteger contra valores undefined
    const missao = {
      icone: item?.icone || '🎯',
      tipo: item?.tipo || 'Missão',
      concluida: item?.concluida || false,
      progresso: item?.progresso || 0,
      meta: item?.meta || 1,
      descricao: item?.descricao || 'Descrição não disponível',
      porcentagem: item?.porcentagem || 0,
      recompensa: item?.recompensa || '50 XP',
      datafim: item?.datafim || null
    };

    return (
      <TouchableOpacity style={getMissaoStyle(missao)}>
        {/* Header da missão */}
        <View style={styles.missaoHeader}>
          <Text style={styles.missaoIcone}>{missao.icone}</Text>
          <View style={styles.missaoInfo}>
            <Text style={styles.missaoTitulo}>{missao.tipo}</Text>
            <Text style={styles.missaoTipo}>{formatarTipo(missao.tipo)}</Text>
          </View>
          <View style={styles.missaoStatus}>
            {missao.concluida ? (
              <Text style={styles.statusConcluida}>✅</Text>
            ) : (
              <Text style={styles.statusProgresso}>{missao.progresso}/{missao.meta}</Text>
            )}
          </View>
      </View>

      {/* Descrição */}
      <Text style={styles.missaoDescricao}>{missao.descricao}</Text>

      {/* Barra de progresso */}
      <View style={styles.progressoContainer}>
        <View style={styles.progressoBar}>
          <View style={getProgressBarStyle(missao.porcentagem)} />
        </View>
        <Text style={styles.progressoTexto}>{Math.round(missao.porcentagem)}%</Text>
      </View>

      {/* Recompensa */}
      <View style={styles.recompensaContainer}>
        <Text style={styles.recompensaLabel}>Recompensa:</Text>
        <Text style={styles.recompensaTexto}>{missao.recompensa}</Text>
      </View>

      {/* Data limite se houver */}
      {missao.datafim && (
        <Text style={styles.dataLimite}>
          Até: {new Date(missao.datafim).toLocaleDateString('pt-BR')}
        </Text>
      )}
    </TouchableOpacity>
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2e7d32" />
        <Text style={styles.loadingText}>Carregando missões...</Text>
      </View>
    )
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Missões</Text>
        <Text style={styles.subtitle}>Complete desafios e ganhe recompensas!</Text>
      </View>

      <FlatList
        data={missoes}
        renderItem={renderMissao}
        keyExtractor={item => (item?.codigo || Math.random()).toString()}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#2e7d32']}
          />
        }
      />
    </View>
  )
}

export default missoes

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#2e7d32',
    fontFamily: 'Montserrat-Regular',
  },
  header: {
    paddingTop: 50,
    paddingHorizontal: 20,
    paddingBottom: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 28,
    fontFamily: 'Montserrat-ExtraBold',
    color: '#2e7d32',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
  },
  listContainer: {
    padding: 20,
  },
  missaoCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    borderLeftWidth: 4,
    borderLeftColor: '#2e7d32',
  },
  missaoConcluida: {
    borderLeftColor: '#4CAF50',
    backgroundColor: '#f8fff8',
  },
  missaoQuaseConcluida: {
    borderLeftColor: '#FF9800',
    backgroundColor: '#fff8f0',
  },
  missaoHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  missaoIcone: {
    fontSize: 32,
    marginRight: 12,
  },
  missaoInfo: {
    flex: 1,
  },
  missaoTitulo: {
    fontSize: 18,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 2,
  },
  missaoTipo: {
    fontSize: 12,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  missaoStatus: {
    alignItems: 'center',
  },
  statusConcluida: {
    fontSize: 24,
  },
  statusProgresso: {
    fontSize: 16,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
  },
  missaoDescricao: {
    fontSize: 14,
    fontFamily: 'Montserrat-Regular',
    color: '#555',
    marginBottom: 16,
    lineHeight: 20,
  },
  progressoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  progressoBar: {
    flex: 1,
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginRight: 12,
    overflow: 'hidden',
  },
  progressoFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressoTexto: {
    fontSize: 12,
    fontFamily: 'Montserrat-Bold',
    color: '#666',
    minWidth: 35,
    textAlign: 'right',
  },
  recompensaContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  recompensaLabel: {
    fontSize: 12,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    marginRight: 8,
  },
  recompensaTexto: {
    fontSize: 12,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    flex: 1,
  },
  dataLimite: {
    fontSize: 11,
    fontFamily: 'Montserrat-Regular',
    color: '#FF5722',
    textAlign: 'right',
    fontStyle: 'italic',
  },
})