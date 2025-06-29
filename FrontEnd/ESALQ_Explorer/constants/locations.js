/**
 * Mapeamento de localizações da ESALQ para coordenadas geográficas
 * Baseado nos nomes das localizações das cartas no banco de dados
 */

export const LOCATIONS_MAP = {
  // Localizações das cartas existentes
  "Prédio Principal - ESALQ": {
    latitude: -22.7085,
    longitude: -47.6305,
    name: "Prédio Principal - ESALQ"
  },
  "Biblioteca Central": {
    latitude: -22.7090,
    longitude: -47.6320,
    name: "Biblioteca Central"
  },
  "Departamento de Ciências Exatas": {
    latitude: -22.7080,
    longitude: -47.6290,
    name: "Departamento de Ciências Exatas"
  },
  "Jardim Botânico": {
    latitude: -22.7095,
    longitude: -47.6310,
    name: "Jardim Botânico"
  },
  "Museu de Mineralogia": {
    latitude: -22.7075,
    longitude: -47.6325,
    name: "Museu de Mineralogia"
  },
  "Departamento de Solos": {
    latitude: -22.7100,
    longitude: -47.6300,
    name: "Departamento de Solos"
  },
  "Observatório Astronômico": {
    latitude: -22.7070,
    longitude: -47.6315,
    name: "Observatório Astronômico"
  },
  "Planetário ESALQ": {
    latitude: -22.7065,
    longitude: -47.6330,
    name: "Planetário ESALQ"
  },
  "Laboratório de Física": {
    latitude: -22.7088,
    longitude: -47.6295,
    name: "Laboratório de Física"
  },
  "Centro de Pesquisas": {
    latitude: -22.7092,
    longitude: -47.6285,
    name: "Centro de Pesquisas"
  },
  "Museu de História Natural": {
    latitude: -22.7078,
    longitude: -47.6340,
    name: "Museu de História Natural"
  }
};

/**
 * Função para obter coordenadas de uma localização
 * @param {string} locationName - Nome da localização
 * @returns {object|null} - Objeto com latitude, longitude e nome ou null se não encontrado
 */
export const getLocationCoordinates = (locationName) => {
  return LOCATIONS_MAP[locationName] || null;
};

/**
 * Função para mapear cartas com suas coordenadas
 * @param {Array} cartas - Array de cartas da coleção
 * @returns {Array} - Array de cartas com coordenadas adicionadas
 */
export const mapCartasWithCoordinates = (cartas) => {
  return cartas.map(carta => {
    const coordinates = getLocationCoordinates(carta.localizacao);
    return {
      ...carta,
      coordinates: coordinates
    };
  }).filter(carta => carta.coordinates !== null); // Remove cartas sem coordenadas conhecidas
};

/**
 * Região padrão da ESALQ para o mapa
 */
export const ESALQ_REGION = {
  latitude: -22.7093,
  longitude: -47.6319,
  latitudeDelta: 0.005,
  longitudeDelta: 0.005,
};

/**
 * Limites geográficos da ESALQ
 */
export const ESALQ_BOUNDS = {
  LAT_MIN: -22.7100,
  LAT_MAX: -22.7000,
  LNG_MIN: -47.6430,
  LNG_MAX: -47.6200
};
