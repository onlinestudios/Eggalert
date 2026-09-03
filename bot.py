import os
from datetime import datetime
from zoneinfo import ZoneInfo

import discord

TOKEN = os.getenv("DISCORD_TOKEN")

SOURCE_CHANNEL_ID = 1544703538125348876
TARGET_CHANNEL_ID = 1545177753983254538
ROLE_ID = 1542801017572163604

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Fang S Egg Alerts is running!")


@bot.event
async def on_message(message):

    # Only watch the SenZ V2 channel
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    # Ignore our own bot
    if bot.user and message.author.id == bot.user.id:
        return

    # SenZ needs to have an embed
    if not message.embeds:
        return

    embed = message.embeds[0]

    # Only process Secret Egg alerts
    title = (embed.title or "").lower()

    if "secret egg" not in title:
        return

    # Read SenZ fields
    data = {}

    for field in embed.fields:
        name = field.name.lower().strip()
        value = field.value.strip()

        # Ignore emojis and identify the field by its text
        if "egg" in name:
            data["egg"] = value

        elif "location" in name:
            data["location"] = value

        elif "money" in name:
            data["money"] = value

        # Spawned is intentionally ignored
        # Recommended Speed is intentionally ignored

    print("SenZ data:", data)

    egg = data.get("egg", "Unknown")
    location = data.get("location", "Unknown")
    money = data.get("money", "Unknown")

    # Remove ~$ from SenZ's money
    money = money.replace("~$", "$").strip()

    # Exact Philippines time when the bot receives the alert
    spawning_time = datetime.now(
        ZoneInfo("Asia/Manila")
    ).strftime("%-I:%M %p")

    # Create your custom embed
    new_embed = discord.Embed(
        title="Fang S | egg alerts",
        description=f"🥚 **Secret {egg} Egg spawned in {location}**",
        color=discord.Color.blurple()
    )

    new_embed.add_field(
        name="Egg",
        value=egg,
        inline=False
    )

    new_embed.add_field(
        name="Location of egg",
        value=location,
        inline=False
    )

    new_embed.add_field(
        name="Spawning time",
        value=spawning_time,
        inline=False
    )

    new_embed.add_field(
        name="Money it makes",
        value=money,
        inline=False
    )

    new_embed.set_footer(
        text="Fang S | Egg Alerts"
    )

    # Send to your real server and ping the role
    try:
        target = await bot.fetch_channel(TARGET_CHANNEL_ID)

        await target.send(
            content=f"<@&{ROLE_ID}>",
            embed=new_embed,
            allowed_mentions=discord.AllowedMentions(
                roles=True
            )
        )

        print("✅ Fang S egg alert sent!")

    except Exception as error:
        print(f"❌ Failed to send alert: {error}")


bot.run(TOKEN)
