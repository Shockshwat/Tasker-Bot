import bot
from discord.ext import tasks
import sqlite3
import datetime
import pytz
import asyncio

client = bot.client
client.load_extension("cogs.upload_task")
client.load_extension("cogs.complete_task")
client.load_extension("cogs.check_task")


async def check_tasks():

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    for task in tasks:
        task_id, user_id, description, deadline, completed = task
        channel = client.get_channel(int(1168899699806322834))

        if not completed:
            await channel.send(
                f"<@{user_id}> Failed to complete task: {task_id} {description}   "
            )
        else:
            await channel.send(f"<@{user_id}> Task Completed: {task_id} {description}")
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    while True:
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        next_9_AM = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now.hour >= 9:  # If it's already past 9 AM, get the next day's 9 AM
            next_9_AM += datetime.timedelta(days=1)
        seconds_until_next_9_AM = (next_9_AM - now).total_seconds()

        await asyncio.sleep(seconds_until_next_9_AM)  # Wait until the next 9 AM
        conn = sqlite3.connect("tasks.db")
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        for task in tasks:
            task_id, user_id, description, deadline, completed = task
            channel = client.get_channel(int(1168899699806322834))

            if not completed:
                await channel.send(
                    f"<@{user_id}> Failed to complete task: {task_id} {description}"
                )
            else:
                await channel.send(
                    f"<@{user_id}> Task Completed: {task_id} {description}"
                )
                c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()


@client.event
async def on_ready():
    client.loop.create_task(check_tasks())
    print("Bot is ready")


client.run(bot.token)
