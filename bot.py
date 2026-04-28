import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run_web)
    server.start()


WELCOME_CHANNEL_ID = 1468641218660667582
ROLE_ID = 1438554888845000784
VERIFY_CHANNEL_ID = 1470498490818756877
GOODBYE_CHANNEL_ID = 1468314237372993749
BOOST_CHANNEL_ID = 1470219129465208905
GUILD_ID = 1438554317647904952

WELCOME_IMAGE_URL = "https://cdn.discordapp.com/attachments/1438554318260146331/1493329315344154796/standard_1.gif"
GOODBYE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1438554318260146331/1493336428321574955/standard_3.gif"
BOOST_IMAGE_URL = "https://cdn.discordapp.com/attachments/1438554318260146331/1493557946729365564/standard_4.gif"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")

    if not update_status.is_running():
        update_status.start()


@tasks.loop(minutes=1)
async def update_status():
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        return

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{guild.member_count} members"
        )
    )


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if not channel:
        print("Channel welcome tidak ditemukan.")
        return

    embed = discord.Embed(
        title="WELCOME",
        description=(
            "°───────── . 𖥔 ݁ ˖\n\n"
            f"➤ **Welcome** : {member.mention}\n"
            f"➤ **Server** : {member.guild.name}\n"
            f"➤ **You are Member** : {member.guild.member_count}\n\n"
            f"Untuk mengambil role <@&{ROLE_ID}>\n"
            f"Verifikasi disini <#{VERIFY_CHANNEL_ID}>\n\n"
            "°───────── . 𖥔 ݁ ˖"
        ),
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=WELCOME_IMAGE_URL)
    embed.set_footer(text="Selamat datang di server!")

    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)

    if not channel:
        print("Channel goodbye tidak ditemukan.")
        return

    embed = discord.Embed(
        title="GOODBYE",
        description=(
            "°───────── . 𖥔 ݁ ˖\n\n"
            f"➤ **User** : {member.name}\n"
            f"➤ **Server** : {member.guild.name}\n"
            f"➤ **Member sekarang** : {member.guild.member_count}\n\n"
            "Semoga kita bertemu lagi 👋\n\n"
            "°───────── . 𖥔 ݁ ˖"
        ),
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_image(url=GOODBYE_IMAGE_URL)
    embed.set_footer(text="Goodbye...")

    await channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    booster_role = after.guild.premium_subscriber_role

    if booster_role is None:
        return

    if booster_role not in before.roles and booster_role in after.roles:
        channel = bot.get_channel(BOOST_CHANNEL_ID)

        if not channel:
            print("Channel boost tidak ditemukan.")
            return

        embed = discord.Embed(
            title="NEW SERVER BOOSTER 💜",
            description=(
                f"Terima kasih {after.mention} sudah boost server!\n"
                f"Total boost: {after.guild.premium_subscription_count}\n"
                f"Level server: {after.guild.premium_tier}"
            ),
            color=discord.Color.magenta()
        )

        embed.set_thumbnail(url=after.display_avatar.url)
        embed.set_image(url=BOOST_IMAGE_URL)

        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    pesan = message.content.lower()

    if pesan == "oi":
        await message.channel.send("# APA WOI")

    elif pesan == "alo":
        await message.channel.send("# SO ASIK AH")

    await bot.process_commands(message)


keep_alive()
bot.run(TOKEN)
