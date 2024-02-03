from discord.ext import commands
import sqlite3


class CheckTasks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="check_tasks", description="Check all pending tasks")
    async def check_tasks(self, ctx):
        # Create a connection to the database
        conn = sqlite3.connect("tasks.db")

        # Create a cursor object
        cursor = conn.cursor()

        # Fetch all pending tasks assigned to the user from the tasks table
        cursor.execute(
            """
            SELECT * FROM tasks
            WHERE completed = 0 AND user_id = ?
        """,
            (ctx.author.id,),
        )  # Use the author's ID as the user ID
        tasks = cursor.fetchall()

        # Close the connection
        conn.close()

        if tasks:
            response = "Here are your pending tasks:\n"
            for task in tasks:
                response += (
                    f"Task ID: {task[0]}, Description: {task[2]}, Deadline: {task[3]}\n"
                )
        else:
            response = "You have no pending tasks."

        await ctx.respond(response)


def setup(client):
    client.add_cog(CheckTasks(client))
