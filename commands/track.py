import discord
from discord.ext import commands
from collections import defaultdict

# Default dict to store per-server user activity
user_thread_activity = defaultdict(lambda: defaultdict(set))

class ThreadTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.Thread):
            user = message.author
            server = message.guild
            thread = message.channel
            user_thread_activity[server.id][user.id].add(thread.id)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if isinstance(channel, discord.Thread):
            if user != channel.owner:
                server = channel.guild
                user_thread_activity[server.id][user.id].add(channel.id)

    @commands.command()
    async def owe(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        server = ctx.guild
        member_id = member.id
        
        active_in = len(user_thread_activity[server.id][member_id])
        owe_replies = len([thread_id for thread_id in user_thread_activity[server.id][member_id] if thread_id != ctx.channel.id])
        
        await ctx.send(f"{member.display_name} is active in {active_in} threads and owes replies in {owe_replies} threads.")

# Allows the cog to be imported and used in main.py
def setup(bot):
    bot.add_cog(ThreadTracker(bot))