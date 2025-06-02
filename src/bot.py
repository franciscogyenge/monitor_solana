import os
import requests
import asyncio
from telegram import Bot

# Configurações
BOT_TOKEN = '8197667864:AAFLHCT9w2U8ERu8mTeatDr1ySg-hY7NGRM'  # Substitua pelo seu token real
CHAT_ID = '7675250716'  # Substitua pelo seu chat_id real

GECKO_TERMINAL_URL = 'https://api.geckoterminal.com/api/v2/networks/solana/pools'
CHECK_INTERVAL = 30  # meio minuto

async def get_new_tokens():
    try:
        response = requests.get(GECKO_TERMINAL_URL)
        if response.status_code == 200:
            data = response.json()
            pools = data.get('data', [])
            return pools
        else:
            print(f"Erro ao acessar GeckoTerminal: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao buscar tokens: {e}")
        return []

async def send_alert(bot, message):
    print(f"Enviando mensagem para chat_id: {CHAT_ID}")
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    print("Bot iniciado e monitorando novas memecoins na Solana.")

    # Envia uma mensagem de teste imediatamente
    await send_alert(bot, "🚀 Bot está funcionando e pronto para monitorar novos tokens na Solana!")

    seen_tokens = set()

    while True:
        pools = await get_new_tokens()
        for pool in pools:
            pool_id = pool.get('id')
            attributes = pool.get('attributes', {})
            if pool_id and pool_id not in seen_tokens:
                seen_tokens.add(pool_id)
                name = attributes.get('token0', {}).get('name') or 'Token sem nome'
                link = f"https://www.geckoterminal.com/solana/pools/{pool_id}"
                liquidity = attributes.get('reserve_in_usd')
                message = f"🚀 Novo token listado na Solana!\n\nNome: {name}\nLiquidez: ${liquidity}\nLink: {link}"
                await send_alert(bot, message)
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(main())
