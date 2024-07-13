import discord
from discord.ext import commands
from collections import defaultdict
user_thread_activity = defaultdict(lambda: {"active_in": set(), "owe_replies": set()})

class ThreadTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.Thread):
            user = message.author
            thread = message.channel
            user_thread_activity[user]["active_in"].add(thread.id)
            if thread.id in user_thread_activity[user]["owe_replies"]:
                user_thread_activity[user]["owe_replies"].remove(thread.id)

    @commands.command()
    async def owe(self, ctx, member: discord.Member):
        active_in = len(user_thread_activity[member]["active_in"])
        owe_replies = len(user_thread_activity[member]["owe_replies"])
        await ctx.send(f"{member.display_name} is active in {active_in} threads and owes replies in {owe_replies} threads.")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if isinstance(channel, discord.Thread):
            if user != channel.owner:
                user_thread_activity[user]["owe_replies"].add(channel.id)

# allows the cog to be imported and used in main.py
def setup(bot):
    bot.add_cog(ThreadTracker(bot))