import AsyncStorage from "@react-native-async-storage/async-storage";
import { BACKEND_URL } from "../constants/api";

class ApiService {
  constructor() {
    this.baseURL = BACKEND_URL;
    this.token = null;
  }

  // Método para definir o token
  setToken(token) {
    this.token = token;
  }

  // Método para obter o token do AsyncStorage
  async getToken() {
    if (!this.token) {
      this.token = await AsyncStorage.getItem("access_token");
    }
    return this.token;
  }

  // Método para limpar o token
  async clearToken() {
    this.token = null;
    await AsyncStorage.removeItem("access_token");
    await AsyncStorage.removeItem("nickname");
  }

  // Método base para fazer requisições
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = await this.getToken();

    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    // Adiciona o token de autorização se existir
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new ApiError(response.status, data, response);
      }

      return { data, response };
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new NetworkError(error.message);
    }
  }

  // Métodos HTTP específicos
  async get(endpoint, options = {}) {
    return this.request(endpoint, { method: "GET", ...options });
  }

  async post(endpoint, body, options = {}) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
      ...options,
    });
  }

  async put(endpoint, body, options = {}) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
      ...options,
    });
  }

  async delete(endpoint, options = {}) {
    return this.request(endpoint, { method: "DELETE", ...options });
  }

  // Métodos específicos da API
  async login(nickname, password) {
    const { data } = await this.post("/login", { nickname, password });

    // Salva o token recebido
    if (data.access_token) {
      await AsyncStorage.setItem("access_token", data.access_token);
      await AsyncStorage.setItem("nickname", nickname);
      this.setToken(data.access_token);
    }

    return data;
  }

  async logout() {
    await this.clearToken();
  }

  // Métodos para cartas
  async getCartas() {
    const { data } = await this.get("/api/cartas");
    return data.data; // O backend retorna { success: true, data: [...] }
  }

  async getCarta(id) {
    const { data } = await this.get(`/api/cartas/${id}`);
    return data.data;
  }

  // Métodos para coleção do usuário
  async getMinhaColecao() {
    const { data } = await this.get("/api/minha-colecao");
    return data.data; // Retorna array de objetos com carta e quantidade
  }

  async adicionarCartaColecao(cartaId) {
    const { data } = await this.post("/api/colecao/adicionar", {
      carta_id: cartaId,
    });
    return data.data;
  }

  async removerCartaColecao(cartaId, quantidade = 1) {
    const { data } = await this.delete("/api/colecao/remover", {
      body: JSON.stringify({ carta_id: cartaId, quantidade }),
    });
    return data.data;
  }

  async getEstatisticasColecao() {
    const { data } = await this.get("/api/colecao/estatisticas");
    return data.data;
  }

  async verificarCarta(cartaId) {
    const { data } = await this.get(`/api/colecao/verificar/${cartaId}`);
    return data.data;
  }

  async limparColecao() {
    const { data } = await this.delete("/api/colecao/limpar");
    return data.data;
  }

  // === MISSÕES ===

  // Buscar todas as missões
  async getMissoes() {
    const { data } = await this.get("/api/missoes");
    return data.data;
  }

  // Buscar participações de quantidade do usuário
  async getParticipacoesQuantidade() {
    const { data } = await this.get("/api/participacoes/quantidade");
    return data.data;
  }

  // Buscar participações de raridade do usuário
  async getParticipacoesRaridade() {
    const { data } = await this.get("/api/participacoes/raridade");
    return data.data;
  }

  // Buscar detalhes de missão por quantidade
  async getMissaoQuantidade(codigo) {
    const { data } = await this.get(`/api/missaoqtd/${codigo}`);
    return data.data;
  }

  // Buscar detalhes de missão por raridade
  async getMissaoRaridade() {
    const { data } = await this.get("/api/missoes/raridade");
    return data.data;
  }

  // Calcular progresso das missões
  async calcularProgressoMissoes() {
    try {
      // Buscar dados necessários
      const [missoes, minhaColecao, participacoesQtd, participacoesRaridade] = await Promise.all([
        this.getMissoes().catch(() => []),
        this.getMinhaColecao().catch(() => []),
        this.getParticipacoesQuantidade().catch(() => []),
        this.getParticipacoesRaridade().catch(() => [])
      ]);
      

      // Validar se os dados são arrays
      const missoesValidas = Array.isArray(missoes) ? missoes : [];
      const colecaoValida = Array.isArray(minhaColecao) ? minhaColecao : [];
      const missoesComProgresso = [];

      for (const missao of missoesValidas) {
        const missaoComProgresso = {
          codigo: missao?.codigo || 0,
          tipo: missao?.tipo || 'Missão',
          educador: missao?.educador || 'Sistema',
          datainicio: missao?.datainicio || new Date(),
          datafim: missao?.dataFim || null,
          progresso: 0,
          meta: 0,
          concluida: false,
          porcentagem: 0,
          descricao: '',
          recompensa: '50 XP',
          icone: '🎯'
        };

        try {
          console.log(`🔍 Processando missão ${missao?.codigo}: ${missao?.tipo}`);
          
          // Primeiro verificar se é missão de quantidade (MissaoQtd)
          const missaoQtd = await this.getMissaoQuantidade(missao?.codigo).catch((error) => {
            console.log(`❌ Erro ao buscar MissaoQtd para código ${missao?.codigo}:`, error);
            return null;
          });
          
          console.log(`📊 MissaoQtd para código ${missao?.codigo}:`, missaoQtd);
          
          if (missaoQtd) {
            // É uma MissaoQtd - calcular baseado na quantidade
            const totalCartas = colecaoValida.reduce((total, item) => total + (item?.quantidade || 0), 0);
            
            missaoComProgresso.meta = missaoQtd?.quantidadetotal || 5;
            missaoComProgresso.progresso = Math.min(totalCartas, missaoComProgresso.meta);
            missaoComProgresso.tipoMissao = 'quantidade';
            
            console.log(`✅ Missão ${missao?.codigo} é do tipo MissaoQtd - Meta: ${missaoComProgresso.meta}, Progresso: ${missaoComProgresso.progresso}`);
            
            // Definir detalhes específicos baseado no tipo
            switch (missao?.tipo) {
              case 'Coletor Iniciante':
                missaoComProgresso.descricao = `Colete suas primeiras ${missaoComProgresso.meta} cartas`;
                missaoComProgresso.icone = '🌱';
                break;
              case 'Explorador':
                missaoComProgresso.descricao = `Colete ${missaoComProgresso.meta} cartas diferentes`;
                missaoComProgresso.icone = '🗺️';
                break;
              case 'Veterano':
                missaoComProgresso.descricao = `Colete ${missaoComProgresso.meta} cartas no total`;
                missaoComProgresso.icone = '🏆';
                break;
              default:
                missaoComProgresso.descricao = `Colete ${missaoComProgresso.meta} cartas`;
                missaoComProgresso.icone = '📦';
                break;
            }
          } else {
            console.log(`🔍 Missão ${missao?.codigo} não é MissaoQtd, verificando MissaoRaridade...`);
            
            // Verificar se é missão de raridade (MissaoRaridade)
            const missoesRaridade = await this.getMissaoRaridade().catch((error) => {
              console.log(`❌ Erro ao buscar MissaoRaridade:`, error);
              return [];
            });
            const missoesRaridadeValidas = Array.isArray(missoesRaridade) ? missoesRaridade : [];
            const missaoRar = missoesRaridadeValidas.find(mr => mr?.codigo === missao?.codigo);
            
            console.log(`📊 MissaoRaridade encontrada para código ${missao?.codigo}:`, missaoRar);
            console.log(`📋 Todas as MissaoRaridade:`, missoesRaridadeValidas);
            
            if (missaoRar || ['Caçador de Raras', 'Lenda Viva', 'Evento Especial'].includes(missao?.tipo)) {
              // É uma MissaoRaridade ou missão especial
              missaoComProgresso.tipoMissao = 'raridade';
              
              console.log(`✅ Missão ${missao?.codigo} é do tipo MissaoRaridade ou especial`);
              
              switch (missao?.tipo) {
                case 'Caçador de Raras':
                  missaoComProgresso.meta = 3;
                  const cartasRaras = colecaoValida.filter(item => 
                    item?.carta && (
                      item.carta?.raridade === 'rara' || 
                      item.carta?.raridade === 'epica' || 
                      item.carta?.raridade === 'lendaria'
                    )
                  );
                  missaoComProgresso.progresso = Math.min(cartasRaras.length, 3);
                  missaoComProgresso.descricao = 'Encontre 3 cartas raras';
                  missaoComProgresso.icone = '⭐';
                  break;
                  
                case 'Lenda Viva':
                  missaoComProgresso.meta = 1;
                  const cartasLendarias = colecaoValida.filter(item => 
                    item?.carta && item.carta?.raridade === 'lendaria'
                  );
                  missaoComProgresso.progresso = cartasLendarias.length > 0 ? 1 : 0;
                  missaoComProgresso.descricao = 'Encontre uma carta lendária';
                  missaoComProgresso.icone = '👑';
                  break;
                  
                case 'Evento Especial':
                  missaoComProgresso.meta = 15;
                  const cartasUnicas = colecaoValida.length;
                  missaoComProgresso.progresso = Math.min(cartasUnicas, 15);
                  missaoComProgresso.descricao = 'Colete 15 cartas durante o evento';
                  missaoComProgresso.icone = '🎉';
                  missaoComProgresso.tipoMissao = 'evento';
                  
                  // Verificar se o evento ainda está ativo
                  const agora = new Date();
                  const fimEvento = missao?.DataFim ? new Date(missao.DataFim) : null;
                  if (fimEvento && agora > fimEvento) {
                    missaoComProgresso.descricao += ' (Evento encerrado)';
                    missaoComProgresso.icone = '⏰';
                  }
                  break;
                  
                default:
                  missaoComProgresso.meta = 1;
                  missaoComProgresso.progresso = 0;
                  missaoComProgresso.descricao = `Complete a missão ${missao?.tipo || 'Especial'}`;
                  missaoComProgresso.icone = '🎯';
                  break;
              }
            } else {
              console.log(`⚠️ Missão ${missao?.codigo} (${missao?.tipo}) não encontrada em MissaoQtd nem MissaoRaridade - usando valores padrão`);
              
              // Missão sem tipo específico - usar valores padrão
              missaoComProgresso.meta = 5;
              missaoComProgresso.progresso = Math.min(colecaoValida.length, 5);
              missaoComProgresso.descricao = `Complete a missão ${missao?.tipo || 'Geral'}`;
              missaoComProgresso.tipoMissao = 'geral';
            }
          }

          // Calcular porcentagem e status
          if (missaoComProgresso.meta > 0) {
            missaoComProgresso.porcentagem = Math.round((missaoComProgresso.progresso / missaoComProgresso.meta) * 100);
            missaoComProgresso.concluida = missaoComProgresso.progresso >= missaoComProgresso.meta;
          }

          // Ajustar recompensa baseada no progresso e tipo de missão
          if (missaoComProgresso.concluida) {
            switch (missaoComProgresso.tipoMissao) {
              case 'raridade':
                missaoComProgresso.recompensa = '200 XP';
                break;
              case 'evento':
                missaoComProgresso.recompensa = '300 XP + Carta Especial';
                break;
              default:
                missaoComProgresso.recompensa = '100 XP';
                break;
            }
          } else if (missaoComProgresso.porcentagem >= 75) {
            missaoComProgresso.recompensa = '75 XP';
          } else if (missaoComProgresso.porcentagem >= 50) {
            missaoComProgresso.recompensa = '50 XP';
          } else {
            missaoComProgresso.recompensa = '25 XP';
          }

        } catch (error) {
          console.warn(`Erro ao processar missão ${missao?.codigo || 'desconhecida'}:`, error);
          // Mantém valores padrão em caso de erro
        }

        missoesComProgresso.push(missaoComProgresso);
      }

      console.log('Missões processadas:', missoesComProgresso.map(m => ({
        codigo: m.codigo,
        tipo: m.tipo,
        progresso: `${m.progresso}/${m.meta}`,
        porcentagem: `${m.porcentagem}%`,
        concluida: m.concluida
      })));

      return missoesComProgresso;

    } catch (error) {
      console.error('Erro ao calcular progresso das missões:', error);
      // Retorna algumas missões de exemplo em caso de erro
      return [
        {
          codigo: 1,
          tipo: 'Coletor Iniciante',
          educador: 'Sistema',
          datainicio: new Date(),
          datafim: null,
          progresso: 0,
          meta: 5,
          tipo: 'quantidade',
          concluida: false,
          porcentagem: 0,
          descricao: 'Colete suas primeiras 5 cartas',
          recompensa: '50 XP',
          icone: '🌱'
        }
      ];
    }
  }

  // === USUÁRIOS ===

  // Buscar estatísticas completas do perfil
  async getProfileStats(nickname) {
    const { data } = await this.get(`/api/usuarios/${nickname}/profile-stats`);
    return data;
  }

  // Buscar leaderboard (ranking dos usuários)
  async getLeaderboard(limit = 10) {
    const { data } = await this.get(
      `/api/usuarios/?limit=${limit}`
    );
    return data;
  }

  // === AMIZADES ===

  // Enviar solicitação de amizade
  async enviarSolicitacaoAmizade(destinatario) {
    const { data } = await this.post("/api/amizades/solicitar", {
      destinatario,
    });
    return data;
  }

  // Aceitar solicitação de amizade
  async aceitarSolicitacaoAmizade(solicitacaoId) {
    const { data } = await this.post(
      `/api/amizades/aceitar/${solicitacaoId}`
    );
    return data;
  }

  // Recusar solicitação de amizade
  async recusarSolicitacaoAmizade(solicitacaoId) {
    const { data } = await this.post(
      `/api/amizades/recusar/${solicitacaoId}`
    );
    return data;
  }

  // Remover amizade
  async removerAmizade(nickname) {
    const { data } = await this.delete(`/api/amizades/remover/${nickname}`);
    return data;
  }

  // Listar meus amigos
  async getMeusAmigos() {
    const { data } = await this.get("/api/amizades/meus-amigos");
    return data;
  }

  // Listar solicitações pendentes
  async getSolicitacoesPendentes() {
    const { data } = await this.get("/api/amizades/solicitacoes-pendentes");
    return data;
  }

  // Buscar usuários
  async buscarUsuarios(termoBusca, limit = 20) {
    const { data } = await this.get(
      `/api/amizades/buscar?q=${encodeURIComponent(
        termoBusca
      )}&limit=${limit}`
    );
    return data;
  }

  // Verificar status de amizade
  async verificarStatusAmizade(nickname) {
    const { data } = await this.get(`/api/amizades/status/${nickname}`);
    return data;
  }

  // Método para verificar se o token ainda é válido
  async validateToken() {
    try {
      await this.get("/api/me");
      return true;
    } catch (error) {
      if (error.status === 401) {
        await this.clearToken();
        return false;
      }
      throw error;
    }
  }

  // Método para buscar dados do usuário atual
  async getCurrentUser() {
    const nickname = await AsyncStorage.getItem("nickname");
    if (!nickname) {
      throw new Error("Usuário não logado");
    }
    return this.get(`/usuarios/${nickname}`);
  }
  // Upload de foto de perfil
  async uploadProfilePhoto(nickname, photoUri) {
    try {
      console.log("Iniciando conversão da imagem para base64...");

      // Converter imagem para base64
      const response = await fetch(photoUri);
      const blob = await response.blob();

      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = async () => {
          try {
            const base64data = reader.result.split(",")[1]; // Remove o prefixo data:image/...;base64,
            console.log("Imagem convertida, enviando para servidor...");

            const { data } = await this.post(
              `/api/usuarios/${nickname}/upload-photo`,
              {
                photo_data: base64data,
              }
            );

            console.log("Resposta do servidor:", data);
            resolve(data);
          } catch (error) {
            console.error("Erro na requisição:", error);
            reject(error);
          }
        };
        reader.onerror = (error) => {
          console.error("Erro ao ler arquivo:", error);
          reject(new Error("Erro ao processar imagem"));
        };
        reader.readAsDataURL(blob);
      });
    } catch (error) {
      console.error("Erro ao fazer upload da foto:", error);
      throw error;
    }
  }
}

// Classes de erro personalizadas
class ApiError extends Error {
  constructor(status, data, response) {
    super("API Error");
    this.name = "ApiError";
    this.status = status;
    this.data = data;
    this.response = response;
  }

  getUserMessage() {
    if (this.status === 401) {
      return "Usuário ou senha incorretos.";
    } else if (this.status === 404) {
      return "Recurso não encontrado.";
    } else if (this.status === 500) {
      return "Erro interno do servidor. Tente novamente mais tarde.";
    } else if (this.data?.detail) {
      const detail = this.data.detail;
      if (typeof detail === "string" && detail.includes("0 rows")) {
        return "Usuário ou senha incorretos.";
      } else if (typeof detail === "object" && detail.message) {
        if (
          detail.message.includes("0 rows") ||
          detail.message.includes("no rows")
        ) {
          return "Usuário ou senha incorretos.";
        }
        return "Erro de autenticação. Verifique suas credenciais.";
      }
      return "Erro de autenticação. Verifique suas credenciais.";
    }
    return "Erro desconhecido. Tente novamente.";
  }
}

class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = "NetworkError";
  }

  getUserMessage() {
    return "Não foi possível conectar ao servidor. Verifique sua conexão com a internet.";
  }
}

// Exporta uma instância singleton
export const apiService = new ApiService();
export { ApiError, NetworkError };
