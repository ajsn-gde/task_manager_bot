import discord
from discord.ext import commands
import database

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_task")
    async def add_task(self, ctx, *, description: str):
        """add a new task with description using embed response."""
        task_id = await database.add_task_db(description)

        embed = discord.Embed(
            title="✨ Task Added",
            description=f"**Description:** {description}",
            color=discord.Color.green()
        )
        embed.add_field(name="Task ID", value=f"`#{task_id}`", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name="show_tasks")
    async def show_tasks(self, ctx):
        """display all saved tasks in a styled embed."""
        tasks = await database.get_all_tasks_db()

        if not tasks:
            embed = discord.Embed(
                title="📋 Task List",
                description="Your task list is empty!",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="📋 Task List",
            color=discord.Color.blue()
        )

        task_list_str = ""
        for task in tasks:
            status = "✅" if task.is_completed else "❌"
            task_list_str += f"`ID: {task.id}` | {status} | {task.description}\n"

        embed.description = task_list_str
        embed.set_footer(text=f"Total tasks: {len(tasks)}")

        await ctx.send(embed=embed)

async def setup(bot):
    # register the cog to the bot instance
    await bot.add_cog(TaskCommands(bot))
    