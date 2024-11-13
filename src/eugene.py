import discord
from discord.ext import commands
from ollama import AsyncClient
import asyncio
import sys

TOKEN = 'YOUR_BOT_TOKEN'

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enables the bot to read message content

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Helper function for logging with flush
def log(message):
    print(message)
    sys.stdout.flush()

@bot.event
async def on_ready():
    log(f"[INFO] Bot is online and logged in as {bot.user}!")

@bot.command()
async def ping(ctx):
    log("[INFO] Received 'ping' command")
    await ctx.send("pong!")
    log("[INFO] Responded to 'ping' command")

@bot.command()
async def eugene(ctx, *, message):
    model_name = "mr-the-plague"
    max_length = 2000  # Discord's character limit
    log(f"[INFO] Received 'eugene' command with message: {message}")

    try:
        client = AsyncClient(host="http://localhost:11434")
        response_content = ""

        async for part in await client.chat(model=model_name, messages=[{"role": "user", "content": message}], stream=True):
            response_content += part['message']['content']

        for i in range(0, len(response_content), max_length):
            await ctx.send(response_content[i:i+max_length])

        log(f"[INFO] Finished processing 'eugene' command for message: {message}")

    except Exception as e:
        error_message = f"Error communicating with Ollama: {e}"
        log(f"[ERROR] {error_message}")
        await ctx.send(error_message)

async def main():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        log(f"[ERROR] Exception in bot runtime: {e}")
    finally:
        log("[INFO] Shutting down bot...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("[INFO] Bot interrupted with keyboard input, exiting...")
    except Exception as e:
        log(f"[CRITICAL] Critical error: {e}")
