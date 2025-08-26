import { default: makeWASocket, useSingleFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from '@whiskeysockets/baileys';
import { Boom } from '@hapi/boom';
import fs from 'fs';

const { state, saveState } = useSingleFileAuthState('./auth_info.json');

async function startBot() {
    const { version } = await fetchLatestBaileysVersion();
    const sock = makeWASocket({
        version,
        auth: state,
    });

    sock.ev.on('creds.update', saveState);

    // Reconexão automática
    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update;
        if(connection === 'close') {
            const reason = new Boom(lastDisconnect?.error)?.output?.statusCode;
            if(reason !== DisconnectReason.loggedOut) {
                startBot(); // reconectar se não deslogado
            }
        } else if(connection === 'open') {
            console.log('Conectado ao WhatsApp!');
        }
    });

    // Enviar mensagem
    const sendMessage = async (jid, message) => {
        await sock.sendMessage(jid, { text: message });
        console.log(`Mensagem enviada para ${jid}: ${message}`);
    };

    // Exemplo: substituir pelo número real do destinatário com o sufixo @s.whatsapp.net
    // Ex: '5591999999999@s.whatsapp.net'
    const numero = '5591999999999@s.whatsapp.net';
    await sendMessage(numero, 'Olá! Teste do bot Baileys');

}

startBot();
