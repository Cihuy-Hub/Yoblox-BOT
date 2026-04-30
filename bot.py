import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

WELCOME_CHANNEL_ID = 1468641218660667582  
ROLE_ID = 1438554888845000784            
VERIFY_CHANNEL_ID = 1470498490818756877  
GOODBYE_CHANNEL_ID = 1468314237372993749
BOOST_CHANNEL_ID = 1470219129465208905
GUILD_ID = 1438554317647904952  


WELCOME_IMAGE_URL = "https://cdn.discordapp.com/attachments/1438554318260146331/1493329315344154796/standard_1.gif?ex=69de92cd&is=69dd414d&hm=04f67096d68b68666c0b4a2920d21509a095cdeedb2c7a104a8fee044e5bcb65&"
GOODBYE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1438554318260146331/1493336428321574955/standard_3.gif?ex=69de996d&is=69dd47ed&hm=7b466fea938f1d2c5ada59a77d01b3d53f137cc6ea6ce2e50971529ca96d4149&"
BOOST_IMAGE_URL   = "https://cdn.discordapp.com/attachments/1438554318260146331/1493557946729365564/standard_4.gif?ex=69df67bb&is=69de163b&hm=6e14b924d9d7c87c883cee3c7e8ed4b273b15b2ce1a2bfc1ce404dbb0ee169a8&"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

import discord
from discord.ext import commands, tasks

@bot.event
async def on_ready():
    print(f"Bot login sebagai {bot.user}")
    update_status.start()

@tasks.loop(minutes=1)
async def update_status():
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        return

    member_count = guild.member_count

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{member_count} members"
        )
    )


@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")


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

    # cek kalau baru boost
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
async def on_ready():
    print(f"Bot login sebagai {bot.user}")
    update_status.start()

@tasks.loop(minutes=1)
async def update_status():
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        return

    member_count = guild.member_count

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{member_count} members"
        )
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "oi":
        await message.channel.send("# APA WOI")

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == "alo":
        await message.channel.send("# SO ASIK AH")

    await bot.process_commands(message)


bot.run(TOKEN)
