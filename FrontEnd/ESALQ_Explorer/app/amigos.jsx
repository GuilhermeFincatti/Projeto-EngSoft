import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Alert,
  Image,
  Modal,
  FlatList
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { apiService } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native';

export default function AmigosScreen() {
  const [activeTab, setActiveTab] = useState('amigos'); // amigos, solicitacoes, buscar
  const [amigos, setAmigos] = useState([]);
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [buscarResultados, setBuscarResultados] = useState([]);
  const [termoBusca, setTermoBusca] = useState('');
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [userNickname, setUserNickname] = useState('');

  useFocusEffect(
    useCallback(() => {
      loadUserData();
      loadAmigos();
      loadSolicitacoesPendentes();
    }, [])
  );

  const loadUserData = async () => {
    try {
      const nickname = await AsyncStorage.getItem('nickname');
      setUserNickname(nickname || '');
    } catch (error) {
      console.error('Erro ao carregar dados do usuário:', error);
    }
  };

  const loadAmigos = async () => {
    try {
      setLoading(true);
      const response = await apiService.getMeusAmigos();
      
      if (response.success) {
        setAmigos(response.data || []);
      } else {
        console.error('Erro ao carregar amigos:', response.error);
      }
    } catch (error) {
      console.error('Erro ao carregar amigos:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSolicitacoesPendentes = async () => {
    try {
      const response = await apiService.getSolicitacoesPendentes();
      
      if (response.success) {
        setSolicitacoes(response.data || []);
      } else {
        console.error('Erro ao carregar solicitações:', response.error);
      }
    } catch (error) {
      console.error('Erro ao carregar solicitações:', error);
    }
  };

  const buscarUsuarios = async () => {
    if (termoBusca.trim().length < 2) {
      setBuscarResultados([]);
      return;
    }

    try {
      setSearchLoading(true);
      const response = await apiService.buscarUsuarios(termoBusca.trim());
      
      if (response.success) {
        // Verificar status de amizade para cada usuário
        const usuariosComStatus = await Promise.all(
          response.data.map(async (usuario) => {
            try {
              const statusResponse = await apiService.verificarStatusAmizade(usuario.nickname);
              return {
                ...usuario,
                statusAmizade: statusResponse.success ? statusResponse.data.status : 'nenhum'
              };
            } catch (error) {
              return {
                ...usuario,
                statusAmizade: 'nenhum'
              };
            }
          })
        );
        setBuscarResultados(usuariosComStatus);
      } else {
        setBuscarResultados([]);
      }
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      setBuscarResultados([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const enviarSolicitacao = async (destinatario) => {
    try {
      const response = await apiService.enviarSolicitacaoAmizade(destinatario);
      
      if (response.success) {
        Alert.alert('Sucesso', 'Solicitação de amizade enviada!');
        // Atualizar status na lista de busca
        setBuscarResultados(prev => 
          prev.map(user => 
            user.nickname === destinatario 
              ? { ...user, statusAmizade: 'pendente' }
              : user
          )
        );
      } else {
        Alert.alert('Erro', response.error || 'Erro ao enviar solicitação');
      }
    } catch (error) {
      console.error('Erro ao enviar solicitação:', error);
      Alert.alert('Erro', 'Erro de conexão. Tente novamente.');
    }
  };

  const aceitarSolicitacao = async (solicitacaoId) => {
    try {
      const response = await apiService.aceitarSolicitacaoAmizade(solicitacaoId);
      
      if (response.success) {
        Alert.alert('Sucesso', 'Solicitação aceita!');
        loadAmigos();
        loadSolicitacoesPendentes();
      } else {
        Alert.alert('Erro', response.error || 'Erro ao aceitar solicitação');
      }
    } catch (error) {
      console.error('Erro ao aceitar solicitação:', error);
      Alert.alert('Erro', 'Erro de conexão. Tente novamente.');
    }
  };

  const recusarSolicitacao = async (solicitacaoId) => {
    try {
      const response = await apiService.recusarSolicitacaoAmizade(solicitacaoId);
      
      if (response.success) {
        Alert.alert('Sucesso', 'Solicitação recusada');
        loadSolicitacoesPendentes();
      } else {
        Alert.alert('Erro', response.error || 'Erro ao recusar solicitação');
      }
    } catch (error) {
      console.error('Erro ao recusar solicitação:', error);
      Alert.alert('Erro', 'Erro de conexão. Tente novamente.');
    }
  };

  const removerAmigo = async (nickname) => {
    Alert.alert(
      'Confirmar',
      `Tem certeza que deseja remover ${nickname} da sua lista de amigos?`,
      [
        { text: 'Cancelar', style: 'cancel' },
        { 
          text: 'Remover', 
          style: 'destructive',
          onPress: async () => {
            try {
              const response = await apiService.removerAmizade(nickname);
              
              if (response.success) {
                Alert.alert('Sucesso', 'Amigo removido');
                loadAmigos();
              } else {
                Alert.alert('Erro', response.error || 'Erro ao remover amigo');
              }
            } catch (error) {
              console.error('Erro ao remover amigo:', error);
              Alert.alert('Erro', 'Erro de conexão. Tente novamente.');
            }
          }
        }
      ]
    );
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await Promise.all([
      loadAmigos(),
      loadSolicitacoesPendentes()
    ]);
    setRefreshing(false);
  };

  const renderAmigo = ({ item }) => (
    <View style={styles.userItem}>
      <View style={styles.avatarContainer}>
        {item.fotoperfil ? (
          <Image source={{ uri: item.fotoperfil }} style={styles.avatar} />
        ) : (
          <View style={[styles.avatar, styles.defaultAvatar]}>
            <Ionicons name="person" size={24} color="#666" />
          </View>
        )}
      </View>

      <View style={styles.userInfo}>
        <Text style={styles.nickname}>{item.nickname}</Text>
        <Text style={styles.ranking}>{item.ranking}</Text>
        <View style={styles.statsContainer}>
          <Text style={styles.statsText}>Nível {item.nivel}</Text>
          <Text style={styles.statsText}>{item.xp} XP</Text>
        </View>
      </View>

      <TouchableOpacity
        style={[styles.actionButton, styles.removeButton]}
        onPress={() => removerAmigo(item.nickname)}
      >
        <Ionicons name="person-remove" size={20} color="#fff" />
      </TouchableOpacity>
    </View>
  );

  const renderSolicitacao = ({ item }) => (
    <View style={styles.userItem}>
      <View style={styles.avatarContainer}>
        {item.fotoperfil ? (
          <Image source={{ uri: item.fotoperfil }} style={styles.avatar} />
        ) : (
          <View style={[styles.avatar, styles.defaultAvatar]}>
            <Ionicons name="person" size={24} color="#666" />
          </View>
        )}
      </View>

      <View style={styles.userInfo}>
        <Text style={styles.nickname}>{item.nickname}</Text>
        <Text style={styles.ranking}>{item.ranking}</Text>
        <View style={styles.statsContainer}>
          <Text style={styles.statsText}>Nível {item.nivel}</Text>
          <Text style={styles.statsText}>{item.xp} XP</Text>
        </View>
      </View>

      <View style={styles.actionsContainer}>
        <TouchableOpacity
          style={[styles.actionButton, styles.acceptButton]}
          onPress={() => aceitarSolicitacao(item.solicitacao_id)}
        >
          <Ionicons name="checkmark" size={20} color="#fff" />
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.actionButton, styles.rejectButton]}
          onPress={() => recusarSolicitacao(item.solicitacao_id)}
        >
          <Ionicons name="close" size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );

  const renderResultadoBusca = ({ item }) => {
    const getButtonProps = () => {
      switch (item.statusAmizade) {
        case 'aceito':
          return {
            text: 'Amigo',
            color: '#4CAF50',
            disabled: true,
            icon: 'checkmark-circle'
          };
        case 'pendente':
          return {
            text: 'Pendente',
            color: '#FF9800',
            disabled: true,
            icon: 'time'
          };
        default:
          return {
            text: 'Adicionar',
            color: '#2196F3',
            disabled: false,
            icon: 'person-add'
          };
      }
    };

    const buttonProps = getButtonProps();

    return (
      <View style={styles.userItem}>
        <View style={styles.avatarContainer}>
          {item.fotoperfil ? (
            <Image source={{ uri: item.fotoperfil }} style={styles.avatar} />
          ) : (
            <View style={[styles.avatar, styles.defaultAvatar]}>
              <Ionicons name="person" size={24} color="#666" />
            </View>
          )}
        </View>

        <View style={styles.userInfo}>
          <Text style={styles.nickname}>{item.nickname}</Text>
          <Text style={styles.ranking}>{item.ranking}</Text>
          <View style={styles.statsContainer}>
            <Text style={styles.statsText}>Nível {item.nivel}</Text>
            <Text style={styles.statsText}>{item.xp} XP</Text>
          </View>
        </View>

        <TouchableOpacity
          style={[
            styles.actionButton,
            { backgroundColor: buttonProps.color },
            buttonProps.disabled && styles.disabledButton
          ]}
          onPress={() => buttonProps.disabled ? null : enviarSolicitacao(item.nickname)}
          disabled={buttonProps.disabled}
        >
          <Ionicons name={buttonProps.icon} size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'amigos':
        return (
          <FlatList
            data={amigos}
            renderItem={renderAmigo}
            keyExtractor={(item) => item.nickname}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
            ListEmptyComponent={
              <View style={styles.emptyState}>
                <Ionicons name="people-outline" size={64} color="#ccc" />
                <Text style={styles.emptyText}>Você ainda não tem amigos</Text>
                <Text style={styles.emptySubtext}>Use a busca para encontrar outros exploradores!</Text>
              </View>
            }
          />
        );

      case 'solicitacoes':
        return (
          <FlatList
            data={solicitacoes}
            renderItem={renderSolicitacao}
            keyExtractor={(item) => item.solicitacao_id.toString()}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
            ListEmptyComponent={
              <View style={styles.emptyState}>
                <Ionicons name="mail-outline" size={64} color="#ccc" />
                <Text style={styles.emptyText}>Nenhuma solicitação pendente</Text>
              </View>
            }
          />
        );

      case 'buscar':
        return (
          <View style={styles.searchContainer}>
            <View style={styles.searchInputContainer}>
              <Ionicons name="search" size={20} color="#666" style={styles.searchIcon} />
              <TextInput
                style={styles.searchInput}
                placeholder="Digite o nickname do usuário..."
                value={termoBusca}
                onChangeText={setTermoBusca}
                onSubmitEditing={buscarUsuarios}
                autoCapitalize="none"
              />
              {termoBusca.length > 0 && (
                <TouchableOpacity
                  onPress={() => {
                    setTermoBusca('');
                    setBuscarResultados([]);
                  }}
                  style={styles.clearButton}
                >
                  <Ionicons name="close-circle" size={20} color="#666" />
                </TouchableOpacity>
              )}
            </View>

            <TouchableOpacity
              style={styles.searchButton}
              onPress={buscarUsuarios}
              disabled={termoBusca.trim().length < 2}
            >
              <Text style={styles.searchButtonText}>Buscar</Text>
            </TouchableOpacity>

            {searchLoading ? (
              <View style={styles.searchLoading}>
                <ActivityIndicator size="small" color="#4CAF50" />
                <Text style={styles.searchLoadingText}>Buscando...</Text>
              </View>
            ) : (
              <FlatList
                data={buscarResultados}
                renderItem={renderResultadoBusca}
                keyExtractor={(item) => item.nickname}
                style={styles.searchResults}
                ListEmptyComponent={
                  termoBusca.length >= 2 ? (
                    <View style={styles.emptyState}>
                      <Ionicons name="search-outline" size={64} color="#ccc" />
                      <Text style={styles.emptyText}>Nenhum usuário encontrado</Text>
                    </View>
                  ) : null
                }
              />
            )}
          </View>
        );

      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="people" size={32} color="#4CAF50" />
        <Text style={styles.title}>Amigos</Text>
        <Text style={styles.subtitle}>Conecte-se com outros exploradores</Text>
      </View>

      {/* Tabs */}
      <View style={styles.tabsContainer}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'amigos' && styles.activeTab]}
          onPress={() => setActiveTab('amigos')}
        >
          <Ionicons 
            name="people" 
            size={20} 
            color={activeTab === 'amigos' ? '#4CAF50' : '#666'} 
          />
          <Text style={[styles.tabText, activeTab === 'amigos' && styles.activeTabText]}>
            Amigos ({amigos.length})
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'solicitacoes' && styles.activeTab]}
          onPress={() => setActiveTab('solicitacoes')}
        >
          <Ionicons 
            name="mail" 
            size={20} 
            color={activeTab === 'solicitacoes' ? '#4CAF50' : '#666'} 
          />
          <Text style={[styles.tabText, activeTab === 'solicitacoes' && styles.activeTabText]}>
            Solicitações ({solicitacoes.length})
          </Text>
          {solicitacoes.length > 0 && (
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{solicitacoes.length}</Text>
            </View>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'buscar' && styles.activeTab]}
          onPress={() => setActiveTab('buscar')}
        >
          <Ionicons 
            name="search" 
            size={20} 
            color={activeTab === 'buscar' ? '#4CAF50' : '#666'} 
          />
          <Text style={[styles.tabText, activeTab === 'buscar' && styles.activeTabText]}>
            Buscar
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      <View style={styles.content}>
        {loading && activeTab !== 'buscar' ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#4CAF50" />
            <Text style={styles.loadingText}>Carregando...</Text>
          </View>
        ) : (
          renderTabContent()
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  tabsContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tab: {
    flex: 1,
    paddingVertical: 16,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    position: 'relative',
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: '#4CAF50',
  },
  tabText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  activeTabText: {
    color: '#4CAF50',
    fontWeight: 'bold',
  },
  badge: {
    backgroundColor: '#FF5722',
    borderRadius: 10,
    paddingHorizontal: 6,
    paddingVertical: 2,
    marginLeft: 4,
    position: 'absolute',
    top: 8,
    right: 8,
  },
  badgeText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  userItem: {
    backgroundColor: '#fff',
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 4,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  avatarContainer: {
    marginRight: 12,
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
  },
  defaultAvatar: {
    backgroundColor: '#e0e0e0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  userInfo: {
    flex: 1,
  },
  nickname: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  ranking: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  statsContainer: {
    flexDirection: 'row',
    marginTop: 4,
  },
  statsText: {
    fontSize: 12,
    color: '#999',
    marginRight: 12,
  },
  actionsContainer: {
    flexDirection: 'row',
  },
  actionButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 8,
  },
  acceptButton: {
    backgroundColor: '#4CAF50',
  },
  rejectButton: {
    backgroundColor: '#F44336',
  },
  removeButton: {
    backgroundColor: '#FF9800',
  },
  disabledButton: {
    opacity: 0.6,
  },
  searchContainer: {
    flex: 1,
    padding: 16,
  },
  searchInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    paddingHorizontal: 16,
    marginBottom: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 16,
    fontSize: 16,
  },
  clearButton: {
    padding: 4,
  },
  searchButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 16,
  },
  searchButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  searchLoading: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  searchLoadingText: {
    marginLeft: 8,
    fontSize: 16,
    color: '#666',
  },
  searchResults: {
    flex: 1,
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 16,
    color: '#ccc',
    marginTop: 16,
    textAlign: 'center',
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
    textAlign: 'center',
  },
});
