import 'dotenv/config';
import makeWASocket, {
  DisconnectReason,
  fetchLatestBaileysVersion,
  useMultiFileAuthState,
} from '@whiskeysockets/baileys';
import pino from 'pino';
import axios from 'axios';

const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:8000';

// memória simples de sessão de conversa (por JID)
const sessions = new Map();

function textFromMessage(msg) {
  const m = msg.message;
  if (!m) return '';
  if (m.conversation) return m.conversation;
  if (m.extendedTextMessage?.text) return m.extendedTextMessage.text;
  if (m.ephemeralMessage?.message?.conversation)
    return m.ephemeralMessage.message.conversation;
  if (m.ephemeralMessage?.message?.extendedTextMessage?.text)
    return m.ephemeralMessage.message.extendedTextMessage.text;
  return '';
}

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState('./auth');
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    auth: state,
    printQRInTerminal: true,          // mostra o QR no terminal
    logger: pino({ level: 'silent' }),// silencioso
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', ({ connection, lastDisconnect }) => {
    if (connection === 'close') {
      const statusCode = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = statusCode !== DisconnectReason.loggedOut;
      console.log('Conexão fechada. Reconnect?', shouldReconnect, statusCode);
      if (shouldReconnect) start();
      else console.log('Sessão deslogada. Apague a pasta ./auth para relogar.');
    } else if (connection === 'open') {
      console.log('✅ Conectado ao WhatsApp');
    }
  });

  sock.ev.on('messages.upsert', async ({ messages, type }) => {
    if (type !== 'notify') return;
    const msg = messages[0];
    if (!msg || msg.key.fromMe) return;

    const jid = msg.key.remoteJid;
    const text = textFromMessage(msg).trim();

    const st = sessions.get(jid) || { step: 'menu', data: {} };

    // MENU INICIAL
    if (st.step === 'menu') {
      if (/^1$/.test(text)) {
        st.step = 'get_name';
        await sock.sendMessage(jid, { text: 'Perfeito! Qual é o seu nome?' });
      } else if (/^2$/.test(text)) {
        await sock.sendMessage(jid, { text: 'Consulta ainda não implementada. Digite 1 para marcar um horário.' });
      } else {
        await sock.sendMessage(jid, {
          text: 'Bem-vindo ao agendador ✂️\n\n1️⃣ Marcar horário\n2️⃣ Consultar agendamento',
        });
      }
      sessions.set(jid, st);
      return;
    }

    // COLETA DE DADOS
    if (st.step === 'get_name') {
      st.data.customer_name = text;
      st.step = 'get_phone';
      await sock.sendMessage(jid, { text: 'Seu telefone (apenas números)?' });
      sessions.set(jid, st);
      return;
    }

    if (st.step === 'get_phone') {
      st.data.phone = text.replace(/\D/g, '');
      st.step = 'get_service';
      await sock.sendMessage(jid, { text: 'Qual serviço? (ex: Corte, Barba, Corte+Barba)' });
      sessions.set(jid, st);
      return;
    }

    if (st.step === 'get_service') {
      st.data.service = text;
      st.step = 'get_datetime';
      await sock.sendMessage(jid, { text: 'Data e hora? (ex: 2025-08-26 15:30)' });
      sessions.set(jid, st);
      return;
    }

    if (st.step === 'get_datetime') {
      const dt = new Date(text.replace(' ', 'T'));
      if (Number.isNaN(dt.getTime())) {
        await sock.sendMessage(jid, { text: 'Formato inválido. Tente: 2025-08-26 15:30' });
        return;
      }
      st.data.start_at = dt.toISOString();
      st.data.notes = st.data.notes || '';

      // Envia pro teu FastAPI
      try {
        const res = await axios.post(`${API_BASE_URL}/appointment/`, st.data);
        const ap = res.data;
        await sock.sendMessage(jid, {
          text:
            `✅ Agendamento criado!\n` +
            `Cliente: ${ap.customer_name}\n` +
            `Serviço: ${ap.service}\n` +
            `Quando: ${ap.start_at}\n` +
            `Telefone: ${ap.phone}`,
        });
      } catch (err) {
        const apiErr = err.response?.data?.detail || err.message;
        await sock.sendMessage(jid, { text: '❌ Erro ao salvar: ' + apiErr });
        console.error('Erro API:', err.response?.data || err);
      }

      sessions.delete(jid);
      await sock.sendMessage(jid, { text: 'Posso ajudar com algo mais? Digite 1 para novo agendamento.' });
      return;
    }
  });

  return sock;
}

start();
