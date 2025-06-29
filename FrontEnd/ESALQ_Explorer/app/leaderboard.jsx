import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  ActivityIndicator,
  Alert,
  Image,
  TouchableOpacity
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { apiService } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function LeaderboardScreen() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [userNickname, setUserNickname] = useState('');
  const [userPosition, setUserPosition] = useState(null);

  useEffect(() => {
    loadLeaderboard();
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const nickname = await AsyncStorage.getItem('nickname');
      setUserNickname(nickname || '');
    } catch (error) {
      console.error('Erro ao carregar dados do usuário:', error);
    }
  };

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await apiService.getLeaderboard(50); // Top 50
      
      if (response.success) {
        setLeaderboard(response.data);
        
        // Encontrar posição do usuário atual
        const nickname = await AsyncStorage.getItem('nickname');
        if (nickname) {
          const userIndex = response.data.findIndex(user => user.nickname === nickname);
          if (userIndex !== -1) {
            setUserPosition(userIndex + 1);
          }
        }
      } else {
        Alert.alert('Erro', 'Não foi possível carregar o ranking');
      }
    } catch (error) {
      console.error('Erro ao carregar leaderboard:', error);
      Alert.alert('Erro', 'Erro de conexão. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadLeaderboard();
    setRefreshing(false);
  };

  const getRankIcon = (position) => {
    switch (position) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return `#${position}`;
    }
  };

  const getRankColor = (position) => {
    switch (position) {
      case 1:
        return '#FFD700'; // Ouro
      case 2:
        return '#C0C0C0'; // Prata
      case 3:
        return '#CD7F32'; // Bronze
      default:
        return '#666';
    }
  };

  const formatXP = (xp) => {
    if (xp >= 1000000) {
      return `${(xp / 1000000).toFixed(1)}M`;
    } else if (xp >= 1000) {
      return `${(xp / 1000).toFixed(1)}K`;
    }
    return xp.toString();
  };

  const renderLeaderboardItem = (user, index) => {
    const position = index + 1;
    const isCurrentUser = user.nickname === userNickname;

    return (
      <View
        key={user.nickname}
        style={[
          styles.rankItem,
          isCurrentUser && styles.currentUserItem,
          position <= 3 && styles.topThreeItem
        ]}
      >
        {/* Posição */}
        <View style={[styles.positionContainer, { borderColor: getRankColor(position) }]}>
          <Text style={[styles.positionText, { color: getRankColor(position) }]}>
            {getRankIcon(position)}
          </Text>
        </View>

        {/* Foto de perfil */}
        <View style={styles.avatarContainer}>
          {user.fotoperfil ? (
            <Image source={{ uri: user.fotoperfil }} style={styles.avatar} />
          ) : (
            <View style={[styles.avatar, styles.defaultAvatar]}>
              <Ionicons name="person" size={24} color="#666" />
            </View>
          )}
        </View>

        {/* Informações do usuário */}
        <View style={styles.userInfo}>
          <Text style={[styles.nickname, isCurrentUser && styles.currentUserText]}>
            {user.nickname}
            {isCurrentUser && ' (Você)'}
          </Text>
          <Text style={styles.ranking}>{user.ranking}</Text>
          <Text style={styles.level}>Nível {user.nivel}</Text>
        </View>

        {/* XP */}
        <View style={styles.xpContainer}>
          <Text style={styles.xpValue}>{formatXP(user.xp)}</Text>
          <Text style={styles.xpLabel}>XP</Text>
        </View>

        {/* Cartas */}
        <View style={styles.cardsContainer}>
          <Ionicons name="albums-outline" size={16} color="#666" />
          <Text style={styles.cardsCount}>{user.qtdcartas}</Text>
        </View>
      </View>
    );
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Carregando ranking...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="trophy" size={32} color="#FFD700" />
        <Text style={styles.title}>Ranking Global</Text>
        <Text style={styles.subtitle}>Top exploradores da ESALQ</Text>
      </View>

      {/* Sua posição */}
      {userPosition && (
        <View style={styles.userPositionCard}>
          <Text style={styles.userPositionText}>
            Sua posição: #{userPosition}
          </Text>
        </View>
      )}

      {/* Lista do ranking */}
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {leaderboard.length > 0 ? (
          leaderboard.map((user, index) => renderLeaderboardItem(user, index))
        ) : (
          <View style={styles.emptyState}>
            <Ionicons name="people-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>Nenhum usuário encontrado</Text>
          </View>
        )}
      </ScrollView>
    </View>
  );
}

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
    color: '#666',
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
  userPositionCard: {
    backgroundColor: '#4CAF50',
    padding: 12,
    margin: 16,
    borderRadius: 8,
    alignItems: 'center',
  },
  userPositionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  scrollView: {
    flex: 1,
    padding: 16,
  },
  rankItem: {
    backgroundColor: '#fff',
    padding: 16,
    marginBottom: 8,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
  },
  currentUserItem: {
    backgroundColor: '#E8F5E8',
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  topThreeItem: {
    backgroundColor: '#FFF9E6',
  },
  positionContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  positionText: {
    fontSize: 16,
    fontWeight: 'bold',
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
    marginRight: 12,
  },
  nickname: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  currentUserText: {
    color: '#4CAF50',
  },
  ranking: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  level: {
    fontSize: 12,
    color: '#999',
    marginTop: 2,
  },
  xpContainer: {
    alignItems: 'center',
    marginRight: 16,
  },
  xpValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FF9800',
  },
  xpLabel: {
    fontSize: 12,
    color: '#666',
  },
  cardsContainer: {
    alignItems: 'center',
    flexDirection: 'row',
  },
  cardsCount: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
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
  },
});
