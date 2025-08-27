import pkg from '@whiskeysockets/baileys';
import Pino from 'pino';

const { default: makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion, DisconnectReason } = pkg;

async function startBot() {
  console.log('⏳ Inicializando Baileys...');
  const { state, saveCreds } = await useMultiFileAuthState('./auth_info');
  console.log('🆗 AuthState carregado.');

  const { version } = await fetchLatestBaileysVersion();
  console.log(`Versão Baileys: ${version}`);

  const sock = makeWASocket({
    version,
    logger: Pino({ level: 'silent' }),
    printQRInTerminal: true,
    auth: state
  });

  sock.ev.on('creds.update', saveCreds);

  sock.ev.on('connection.update', (update) => {
    console.log('⤵ Update de conexão:', update.connection);
    if (update.connection === 'open') {
      console.log('✅ Conectado com sucesso! :)');
      // Enviando uma mensagem de teste opcional:
      sock.sendMessage('559999999999@s.whatsapp.net', { text: 'Bot conectado!' })
        .catch(console.error);
    }
    if (update.connection === 'close') {
      console.log('⚠️ Conexão fechada, tentando reconectar...');
      startBot();
    }
  });

  sock.ev.on('messages.upsert', ({ messages }) => {
    const msg = messages[0];
    const from = msg.key.remoteJid;
    const text = msg.message?.conversation || '';
    console.log(`📩 [${from}] → ${text}`);
    if (text.toLowerCase() === 'ping') {
      sock.sendMessage(from, { text: 'pong 🏓' })
        .catch(console.error);
    }
  });
}

startBot();
