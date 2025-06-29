import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Dimensions } from 'react-native'
import React from 'react'
import { useRouter } from 'expo-router'
import QRCode from 'react-native-qrcode-svg'

const { width } = Dimensions.get('window')
const qrSize = width * 0.4

const TestQRCodes = () => {
  const router = useRouter()
  
  const cartas = [
    { qrcode: "QR001", nome: "Carta do Sol", raridade: "comum", cor: "#4CAF50" },
    { qrcode: "QR002", nome: "Carta da Lua", raridade: "rara", cor: "#FFD700" },
    { qrcode: "QR003", nome: "Carta de Mercúrio", raridade: "comum", cor: "#4CAF50" },
    { qrcode: "QR004", nome: "Carta de Vênus", raridade: "incomum", cor: "#FF9800" },
    { qrcode: "QR005", nome: "Carta da Terra", raridade: "rara", cor: "#FFD700" },
    { qrcode: "QR006", nome: "Carta de Marte", raridade: "incomum", cor: "#FF9800" },
    { qrcode: "QR007", nome: "Carta de Júpiter", raridade: "lendária", cor: "#FF5722" },
    { qrcode: "QR008", nome: "Carta de Saturno", raridade: "lendária", cor: "#FF5722" },
    { qrcode: "QR009", nome: "Carta de Urano", raridade: "épica", cor: "#9C27B0" },
    { qrcode: "QR010", nome: "Carta de Netuno", raridade: "épica", cor: "#9C27B0" },
    { qrcode: "QR011", nome: "Carta de Plutão", raridade: "rara", cor: "#FFD700" }
  ]

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🎴 QR Codes de Teste</Text>
        <Text style={styles.subtitle}>
          Escaneie estes códigos para testar a coleta de cartas
        </Text>
        
        <TouchableOpacity 
          style={styles.scanButton}
          onPress={() => router.push('/camera')}
        >
          <Text style={styles.scanButtonText}>📷 Abrir Scanner</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.grid}>
        {cartas.map((carta, index) => (
          <View key={carta.qrcode} style={[styles.cartaContainer, { borderColor: carta.cor }]}>
            <View style={styles.qrContainer}>
              <QRCode
                value={carta.qrcode}
                size={qrSize}
                backgroundColor="white"
                color="black"
              />
            </View>
            <Text style={styles.cartaNome}>{carta.nome}</Text>
            <Text style={styles.cartaCodigo}>{carta.qrcode}</Text>
            <View style={[styles.raridade, { backgroundColor: carta.cor }]}>
              <Text style={styles.raridadeText}>{carta.raridade.toUpperCase()}</Text>
            </View>
          </View>
        ))}
      </View>
      
      <View style={styles.instrucoes}>
        <Text style={styles.instrucoesTitle}>📋 Como testar:</Text>
        <Text style={styles.instrucoesText}>
          1. Toque em "Abrir Scanner" acima{'\n'}
          2. Aponte a câmera para qualquer QR code desta tela{'\n'}
          3. Aguarde o app reconhecer e coletar a carta{'\n'}
          4. Verifique sua coleção para ver a carta adicionada
        </Text>
      </View>
    </ScrollView>
  )
}

export default TestQRCodes

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
    fontFamily: 'Montserrat-ExtraBold',
    color: '#2e7d32',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    textAlign: 'center',
    marginBottom: 20,
  },
  scanButton: {
    backgroundColor: '#2e7d32',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
  },
  scanButtonText: {
    color: '#fff',
    fontSize: 16,
    fontFamily: 'Montserrat-Bold',
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    padding: 10,
  },
  cartaContainer: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 15,
    margin: 10,
    alignItems: 'center',
    borderWidth: 3,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    width: width * 0.42,
  },
  qrContainer: {
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 10,
    marginBottom: 10,
  },
  cartaNome: {
    fontSize: 14,
    fontFamily: 'Montserrat-Bold',
    color: '#333',
    textAlign: 'center',
    marginBottom: 5,
  },
  cartaCodigo: {
    fontSize: 12,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    marginBottom: 8,
  },
  raridade: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  raridadeText: {
    color: '#fff',
    fontSize: 10,
    fontFamily: 'Montserrat-Bold',
  },
  instrucoes: {
    backgroundColor: '#fff',
    margin: 20,
    padding: 20,
    borderRadius: 15,
    borderLeftWidth: 5,
    borderLeftColor: '#2e7d32',
  },
  instrucoesTitle: {
    fontSize: 18,
    fontFamily: 'Montserrat-Bold',
    color: '#2e7d32',
    marginBottom: 10,
  },
  instrucoesText: {
    fontSize: 14,
    fontFamily: 'Montserrat-Regular',
    color: '#666',
    lineHeight: 20,
  },
})
