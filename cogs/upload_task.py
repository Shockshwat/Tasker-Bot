import bot
import discord
from discord.ext import commands, tasks
from discord import option
import random
import datetime
import sqlite3
import pytz
import asyncio

client = bot.client


class UploadTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="upload_task", description="Upload a task to the task list"
    )
    @option(name="User", description="The user to upload the task to", required=True)
    @option(name="task", description="The task to upload", required=True)
    async def upload_task(self, ctx, task: str, user: discord.Member):
        # Generate a random task ID

        # Generate a 6-digit task ID
        task_id = random.randint(100000, 999999)

        # Create a connection to the database
        conn = sqlite3.connect("tasks.db")

        # Create a cursor object
        cursor = conn.cursor()

        # Get the current time in +5:30 GMT
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

        # Set the deadline to 9:00 AM +5:30 GMT on the next day
        if now.hour >= 12:
            deadline = now + datetime.timedelta(days=1)
        else:
            deadline = now
        deadline = deadline.replace(hour=9, minute=0, second=0, microsecond=0)

        # Add the task to the tasks table
        cursor.execute(
            """
            INSERT INTO tasks (id, user_id, description, deadline, completed)
            VALUES (?, ?, ?, ?, ?)
        """,
            (task_id, user.id, task, deadline.isoformat(), 0),
        )

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()

        await client.get_channel(1203367237235253269).send(
            f"{user.mention} You have a new task! ID: {task_id} \n ```{task}```"
        )
        await ctx.respond(
            f"Task {task} with ID {task_id} has been uploaded to the task list",
        )

    @tasks.loop(hours=24)
    async def check_tasks(self):
        # Get the current time in +5:30 GMT
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

        # Check the tasks at 9:00 AM +5:30 GMT every day
        if now.hour == 9:
            # Create a connection to the database
            conn = sqlite3.connect("tasks.db")

            # Create a cursor object
            cursor = conn.cursor()

            # Get the list of tasks
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()

            # Check each task
            for task in tasks:
                task_id, user_id, description, deadline, completed = task

                # If the task has not been completed, send a "Failure to complete task" message and issue a punishment
                if not completed:
                    await client.get_channel(1168899699806322834).send(
                        f"<@{user_id}> Failed to complete task {task_id}: {description}"
                    )
                    # Issue a punishment here

                # If the task has been completed, send a "Task Completed" message
                else:
                    await client.get_channel(1168899699806322834).send(
                        f"<@{user_id}> Completed Task {task_id}: {description}"
                    )

            # Close the connection
            conn.close()

    @check_tasks.before_loop
    async def before_check_tasks(self):
        await self.client.wait_until_ready()

        # If the bot starts after 9:00 AM, the first check should be done immediately
        now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        if now.hour >= 9:
            return

        # If the bot starts before 9:00 AM, the first check should be done at 9:00 AM
        delta = datetime.timedelta(hours=9) - now.time()
        await asyncio.sleep(delta.seconds)


def setup(client):
    client.add_cog(UploadTask(client))
