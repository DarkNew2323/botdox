import nest_asyncio
nest_asyncio.apply()

import asyncio
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURACIÓN ---
api_id = 27361189
api_hash = 'c69474dced272452b876c138df121a73'
BOT_TOKEN = '8119897838:AAEXt_tQm-9KEMJCSmCtPCoGmRLRK2ZEmsQ'
BOT_EXTERNO_USERNAME = 'DoxINVESTIGACION_BOT'

# --- Cliente Telethon (usuario) ---
telethon_client = TelegramClient('user_session', api_id, api_hash)

async def enviar_comando_telethon(comando: str) -> str:
    """
    Envía el comando al bot externo y espera la respuesta final.
    """
    mensajes = []
    response_event = asyncio.Event()

    @telethon_client.on(events.NewMessage(chats=BOT_EXTERNO_USERNAME))
    async def handler(event):
        mensajes.append(event.raw_text)
        response_event.set()

    await telethon_client.send_message(BOT_EXTERNO_USERNAME, comando)

    while True:
        response_event.clear()
        try:
            await asyncio.wait_for(response_event.wait(), timeout=3)
        except asyncio.TimeoutError:
            break

    telethon_client.remove_event_handler(handler)

    return "\n\n".join(mensajes) if mensajes else "No se recibió respuesta del bot externo."

# --- Funciones del bot propio ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Envíame un comando como /dnix 44443333 y lo enviaré al bot externo.")

async def comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Por favor usa el comando así: /dnix 44443333")
        return

    comando_texto = ' '.join(context.args)
    await update.message.reply_text(f"Enviando comando al bot externo: {comando_texto}")
    respuesta = await enviar_comando_telethon(comando_texto)
    await update.message.reply_text(f"Respuesta del bot externo:\n{respuesta}")

async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = """<b>[🧠 COMANDOS DISPONIBLES]</b>

<b>[🪪] RENIEC ONLINE - FREE</b>
Comando ➾ <code>/dnix 44443333</code>
Precio ➾ Gratis
Resultado ➾ Foto e información media en (TEXTO).

<b>[🔍] NOMBRE FILTER - FREE</b>
Comando ➾ <code>/nm N¹|AP¹|AP²</code>
Precio ➾ Gratis
Resultado ➾ Filtrador de Nombres en (TEXTO Y TXT).

<b>[📞] OSIPTEL DATABASE - FREE</b>
Comando ➾ <code>/tel 44443333</code>
Comando ➾ <code>/tel 999888777</code>
Precio ➾ Gratis
Resultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).

<b>[📞] OSIPTEL OPERADOR - FREE</b>
Comando ➾ <code>/op 999888777</code>
Precio ➾ Gratis
Resultado ➾ Devuelve el operador desde OSIPTEL en (TEXTO).

<b>[📞] OSIPTEL VERIFICADOR - FREE</b>
Comando ➾ <code>/osipver 44443333</code>
Precio ➾ Gratis
Resultado ➾ Devuelve las líneas desde OSIPTEL en (TEXTO).

<b>[💳] YAPE FAKE - GRATIS</b>
Comando ➾ <code>/yape 10|LUIS PEDRO|1</code>
Precio ➾ Gratis
Resultado ➾ Genera un baucher fake en (FOTO).
"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=mensaje,
        parse_mode="HTML"
    )

# --- Función principal ---
async def main():
    await telethon_client.start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dnix", comando))
    app.add_handler(CommandHandler("nm", comando))
    app.add_handler(CommandHandler("tel", comando))
    app.add_handler(CommandHandler("op", comando))
    app.add_handler(CommandHandler("osipver", comando))
    app.add_handler(CommandHandler("yape", comando))
    app.add_handler(CommandHandler("comandos", comandos))

    print("🤖 Bot propio corriendo...")
    await app.run_polling()

# --- Ejecutar ---
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
