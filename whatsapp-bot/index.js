// index.js
import * as baileys from '@whiskeysockets/baileys'
import Pino from 'pino';
import qrcode from 'qrcode-terminal';
import dotenv from 'dotenv';

dotenv.config()

async function startBot() {
    console.log('Inicializando Baileys...');

    // Carrega ou cria auth state na pasta auth_info
    const { state, saveCreds } = await baileys.useMultiFileAuthState('./auth_info');

    // Busca versão atual do WhatsApp Web
    const { version } = await baileys.fetchLatestBaileysVersion();

    // Cria socket
    const sock = baileys.makeWASocket({
        version,
        auth: state,
        logger: Pino({ level: 'silent' }),
    });

    // Eventos de conexão
    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('QR Code gerado! Escaneie com o WhatsApp:');
            qrcode.generate(qr, { small: true });
        }

        console.log('Status de conexão:', connection);

        if (connection === 'close') {
            const reason = lastDisconnect?.error?.output?.statusCode;
            console.log('Desconectado, motivo:', reason);
            startBot(); // reconectar automaticamente
        }

        if (connection === 'open') {
            console.log('✅ Conectado com sucesso!');
        }
    });

    // Evento de recebimento de mensagens
    sock.ev.on('messages.upsert', (m) => {
        console.log('Mensagem recebida:', JSON.stringify(m, null, 2));
    });

    // Atualização de credenciais
    sock.ev.on('creds.update', saveCreds);
}

startBot();
