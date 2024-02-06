import discord
from discord.ext import commands
intents = discord.Intents.all()
from webserver import keep_alive
import io
bot = commands.Bot(command_prefix="!",intents=intents)

# Define the user and channel IDs
user_id_to_monitor = 1138617898127073351
target_channel_id = 1160060293150412800



keep_alive()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.id == user_id_to_monitor and message.guild is None:
        # Check if the message is from the specified user and is a direct message
        channel = bot.get_channel(target_channel_id)
        if channel is not None:
            forwarded_message = f"{message.content}"
            
            # Check for attachments (images)
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                        # If it's an image file, send the image directly
                        file_data = await attachment.read()
                        await channel.send(forwarded_message, file=discord.File(fp=io.BytesIO(file_data), filename=attachment.filename))
                    else:
                        # If it's not an image, send a link to the attachment
                        forwarded_message += f"\nStock: {attachment.url}"
            
            if not message.attachments or not any(attachment.url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")) for attachment in message.attachments):
                # If there are no image attachments, send the message without an attachment
                await channel.send(forwarded_message)

    await bot.process_commands(message)

# Run the bot
import os

bot.run(os.environ['tkn'])
