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

        # Send the task completion information to a verification channel
        verification_channel = self.client.get_channel(
            1168899699806322834
        )  # Replace with your verification channel ID
        verification_message = await verification_channel.send(
            f"Task {task_id} has been marked as completed with message and image : {message} {image}\n"
            "React with ✅ if the task has been done or ❌ if the task is not deemed completed."
        )

        # Add a tick and cross reactions to the verification message
        await verification_message.add_reaction("✅")
        await verification_message.add_reaction("❌")
        await ctx.respond("Task has been sent for verification.")

        # Wait for a reaction to the verification message
        def check(reaction, user):
            return (
                user != self.client.user
                and reaction.message.id == verification_message.id
                and str(reaction.emoji) in ["✅", "❌"]
            )

        reaction, user = await self.client.wait_for("reaction_add", check=check)

        if str(reaction.emoji) == "✅":
            # If the reaction is a tick, mark the task as completed in the tasks table
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

            await ctx.send(
                f"Task {task_id} has been marked as completed by the operator {user.mention}.",
            )
        else:
            # If the reaction is a cross, do not mark the task as completed
            await ctx.send(
                f"Task {task_id} has not been marked as completed. Please try again.",
            )

        # Close the connection
        conn.close()


def setup(client):
    client.add_cog(CompleteTask(client))
