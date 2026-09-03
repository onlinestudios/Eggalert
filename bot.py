import os
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
    # Only listen to the SenZ V2 channel
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    # Ignore our own messages
    if message.author == bot.user:
        return

    # We need SenZ's embed
    if not message.embeds:
        return

    embed = message.embeds[0]

    # Get SenZ fields
    data = {}

    for field in embed.fields:
        data[field.name.lower().strip()] = field.value

    # Ignore anything that isn't an egg alert
    if "egg" not in data:
        return

    egg = data.get("egg", "Unknown")
    location = data.get("location", "Unknown")
    spawned = data.get("spawned", "Just now")
    money = data.get("money", "Unknown")

    # Remove ~$ if SenZ included it
    money = money.replace("~$", "$")

    # Send your custom embed
    new_embed = discord.Embed(
        title="Fang S | egg alerts",
        description=f"🥚 **Secret {egg} Egg spawned in {location}**",
        color=discord.Color.blurple()
    )

    new_embed.add_field(name="Egg", value=egg, inline=False)
    new_embed.add_field(name="Location of egg", value=location, inline=False)
    new_embed.add_field(name="Spawning time", value=spawned, inline=False)
    new_embed.add_field(name="Money it makes", value=money, inline=False)

    new_embed.set_footer(text="Fang S | Egg Alerts")

    target = bot.get_channel(TARGET_CHANNEL_ID)

    if target:
        await target.send(
            content=f"<@&{ROLE_ID}>",
            embed=new_embed,
            allowed_mentions=discord.AllowedMentions(roles=True)
        )


bot.run(TOKEN)
