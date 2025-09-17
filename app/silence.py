import discord
from discord.ext import commands
import time
import asyncio
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
MENTION_ID = int(os.getenv("MENTION_ID"))
MUTE_ROLE_NAME = "Silence"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
user_messages = defaultdict(list)
muted_users_roles = {}
reported_users = set()

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

    for guild in bot.guilds:
        mute_role = discord.utils.get(guild.roles, name=MUTE_ROLE_NAME)
        if not mute_role:
            try:
                await guild.create_role(name=MUTE_ROLE_NAME, reason="Rôle pour mute les spammeurs")
                print(f" Rôle '{MUTE_ROLE_NAME}' créé sur {guild.name}.")
            except Exception as e:
                print(f" Impossible de créer le rôle '{MUTE_ROLE_NAME}' : {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.guild is None:
        return

    guild = message.guild
    member = guild.get_member(message.author.id)
    if not member:
        return

    now = time.time()
    content = message.content.lower().strip()
    channel_id = message.channel.id


    user_messages[message.author.id].append((content, now, message, channel_id))


    user_messages[message.author.id] = [
        (msg, timestamp, msg_obj, chan_id)
        for msg, timestamp, msg_obj, chan_id in user_messages[message.author.id]
        if now - timestamp <= 300
    ]

    identical_messages = [msg for msg, _, _, _ in user_messages[message.author.id] if msg == content]
    should_mute = len(identical_messages) >= 3

    if should_mute and member.id not in reported_users:
        reported_users.add(member.id)

        mute_role = discord.utils.get(guild.roles, name=MUTE_ROLE_NAME)
        if not mute_role:
            try:
                mute_role = await guild.create_role(name=MUTE_ROLE_NAME, reason="Rôle pour mute les spammeurs")
            except Exception as e:
                print(f"️Impossible de créer le rôle '{MUTE_ROLE_NAME}' : {e}")
                return

        muted_users_roles[member.id] = [role for role in member.roles if role != guild.default_role]
        try:
            await member.remove_roles(*muted_users_roles[member.id], reason="Mute pour spam")
            await member.add_roles(mute_role, reason="Spam détecté")
        except Exception as e:
            print(f"Erreur lors du mute de {member}: {e}")
            return

        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"<@{MENTION_ID}> {member.mention} a été mute pour spam ! \n\n"
                f"Message spam : `{content}`\n\n"
                f"Tapez `!Silence {member.mention}` pour lui redonner ses rôles."
            )

        
        deletion_time_limit = now - 300
        for msg, timestamp, msg_obj, _ in user_messages[message.author.id]:
            if deletion_time_limit <= timestamp <= now and msg == content:
                try:
                    await msg_obj.delete()
                except Exception as e:
                    print(f"Erreur suppression message: {e}")

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def Silence(ctx, member: discord.Member):
    """Unmute un utilisateur et lui redonne ses rôles."""
    mute_role = discord.utils.get(ctx.guild.roles, name=MUTE_ROLE_NAME)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if member.id in muted_users_roles:
        try:
            if mute_role and mute_role in member.roles:
                await member.remove_roles(mute_role, reason="Unmute par un admin")

            if muted_users_roles[member.id]:
                await member.add_roles(*muted_users_roles[member.id], reason="Retour des rôles")

            del muted_users_roles[member.id]
            reported_users.discard(member.id)

            if log_channel:
                await log_channel.send(f"✅ {member.mention} a été unmute et a récupéré ses rôles !")

        except discord.Forbidden:
            print("Erreur de permissions pour unmute.")
        except Exception as e:
            print(f"Erreur lors de l’unmute : {e}")

bot.run(os.getenv("TOKEN"))
