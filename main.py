import bot

client = bot.client


@client.event
async def on_ready():
    print("Bot is ready")


client.load_extension("cogs.upload_task")
client.load_extension("cogs.complete_task")
client.load_extension("cogs.check_task")
client.run(bot.token)
