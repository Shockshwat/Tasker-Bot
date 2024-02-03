from discord.ext import commands
from discord import option
import sqlite3
import discord


class CompleteTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="complete_task", description="Mark a task as completed"
    )
    @option(
        name="Task_ID",
        description="The ID of the task to mark as completed",
        required=True,
    )
    @option(name="Proof Image", description="Confirmation", required=True)
    @option(name="Message", description="Confirmation", required=True)
    async def complete_task(
        self, ctx, image: discord.Attachment, message: str, task_id: str
    ):
        # Create a connection to the database
        conn = sqlite3.connect("tasks.db")

        # Create a cursor object
        cursor = conn.cursor()

        # Mark the task as completed in the tasks table
        cursor.execute(
            """
            UPDATE tasks
            SET completed = 1
            WHERE id = ?
        """,
            (task_id,),
        )

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()

        await ctx.respond(
            f"Task {task_id} has been marked as completed with message and image : {message} {image}",
        )


def setup(client):
    client.add_cog(CompleteTask(client))
