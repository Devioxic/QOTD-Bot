import discord
from discord.ext import commands, tasks
from discord.ext.pages import Paginator, Page
from discord import option
from Utils.data import Data


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = Data()

    def can_use_command(self, member: discord.Member):
        if member.guild_permissions.administrator:
            return True
        for role in member.roles:
            if self.data.check_allowed_role(role.id):
                return True
        return False
    
    async def no_perms(self, ctx):
        await ctx.respond("You do not have permission to use this command", ephemeral=True)

    @commands.slash_command(
        name="add_question", description="Add a question to be asked"
    )
    async def add_question(self, ctx, question: str):
        if not self.can_use_command(ctx.author):
            await self.no_perms(ctx)
            return
        
        if self.data.check_existing_question(question):
            await ctx.respond("Question already exists!", ephemeral=True)
            return
        self.data.add_question(question)
        await ctx.respond("Question added!", ephemeral=True)

    @commands.slash_command(
        name="remove_question", description="Remove a question from the list"
    )
    @option(
        name="id",
        description="The id of the question to remove",
        required=True,
        type=int,
    )
    async def remove_question(self, ctx, id: int):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
        try:
            self.data.remove_question(id)
        except:
            await ctx.respond("Question not found!", ephemeral=True)
            return
        await ctx.respond("Question removed!", ephemeral=True)

    @commands.slash_command(name="get_questions", description="see all questions")
    async def get_questions(self, ctx):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        questions = self.data.get_all_questions()

        if not questions:
            await ctx.respond("No questions found!", ephemeral=True)
            return

        embeds = []

        for i, question in questions.items():
            question = question.decode("utf-8")
            if i == 0 or i % 5 == 0 or not embeds[len(embeds) - 1]:
                embed = discord.Embed(title="Questions", color=discord.Color.red())
                embeds.append(embed)

            embeds[len(embeds) - 1].add_field(
                name=f"Question #{i}", value=question, inline=False
            )

        pages = []
        for embed in embeds:
            pages.append(Page(embeds=[embed]))

        paginator = Paginator(pages=pages, author_check=True, loop_pages=False)
        await paginator.respond(interaction=ctx.interaction, ephemeral=True)

    @commands.slash_command(
        name="add_allowed_role", description="Add a role that can use the bot"
    )
    @option(
        name="role", description="The role to add", required=True, type=discord.Role
    )
    async def add_allowed_role(self, ctx, role: discord.Role):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        if self.data.check_allowed_role(role.id):
            await ctx.respond("Role already exists!", ephemeral=True)
            return
        self.data.add_allowed_role(role.id)
        await ctx.respond("Role added!", ephemeral=True)

    @commands.slash_command(
        name="remove_allowed_role", description="Remove a role that can use the bot"
    )
    @option(
        name="role", description="The role to remove", required=True, type=discord.Role
    )
    async def remove_allowed_role(self, ctx, role: discord.Role):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        if not self.data.check_allowed_role(role.id):
            await ctx.respond("Role not found!", ephemeral=True)
            return
        self.data.remove_allowed_role(role.id)
        await ctx.respond("Role removed!", ephemeral=True)

    @commands.slash_command(
        name="get_allowed_roles", description="See all roles that can use the bot"
    )
    async def get_allowed_roles(self, ctx):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        roles = self.data.get_allowed_roles()
        print(roles)

        embeds = []

        i = 0
        for role in roles:
            decoded = role.decode("utf-8")
            role = ctx.guild.get_role(int(decoded))
            if i == 0 or i % 5 == 0 or not embeds[len(embeds) - 1]:
                embed = discord.Embed(title="Allowed Roles", color=discord.Color.red())
                embeds.append(embed)

            embeds[len(embeds) - 1].add_field(
                name=f" ", value=role.mention, inline=False
            )
            i += 1

        pages = []

        for embed in embeds:
            pages.append(Page(embeds=[embed]))

        paginator = Paginator(pages=pages, author_check=True, loop_pages=False)
        await paginator.respond(interaction=ctx.interaction, ephemeral=True)

    @commands.slash_command(
        name="set_channel",
        description="Set the channel where the bot will ask questions",
    )
    @option(
        name="channel",
        description="The channel to set",
        required=True,
        type=discord.TextChannel,
    )
    async def set_channel(self, ctx, channel: discord.TextChannel):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        self.data.set_channel(channel.id)
        await ctx.respond("Channel set!", ephemeral=True)

    async def get_channel(self, ctx):
        if not self.can_use_command(ctx.author):
                    await self.no_perms(ctx)
                    return
                
        channel = self.data.get_channel()
        if not channel:
            await ctx.respond("*WARNING* Channel not set!", ephemeral=True)
            return
        ctx.respond(f"QOTD will be asked in <#{channel}>", ephemeral=True)


def setup(bot):
    bot.add_cog(Commands(bot))
