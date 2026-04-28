import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Flask keep alive
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# =========================
# DISCORD BOT SETUP
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# =========================
# FLASK KEEP ALIVE
# =========================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

@app.route('/health')
def health():
    return "OK"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# =========================
# RUN BOT + WEB
# =========================
keep_alive()
bot.run(TOKEN)
