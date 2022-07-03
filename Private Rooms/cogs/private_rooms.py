from disnake.ext import commands
import disnake as discord
from utils.logger import *

texts = {
    "🖊️": {"start": "ручка", "end": "енд ручка"},
    "👥": {"start": "юзеры", "end": ""},
    "🔒": {"start": "замочек", "end": ""},
    "🔓": {"start": "анлок", "end": ""},
    "🚪": {"start": "дверь", "end": ""},
    "✔": {"start": "галочка", "end": ""},
    "❌": {"start": "крест", "end": ""},
    "🔉": {"start": "звук", "end": ""},
    "🔇": {"start": "звук офф", "end": ""},
    "👑": {"start": "корона", "end": ""}
}


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @discord.ui.button(label="", emoji="🖊️")
    async def _pan(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="👥")
    async def _users(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="🔒")
    async def _lock(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="🔓")
    async def _unlock(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="🚪")
    async def _dver(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="✔")
    async def _dat(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="❌")
    async def _nedat(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="🔉")
    async def _unmute(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="🔇")
    async def _mute(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass

    @discord.ui.button(label="", emoji="👑")
    async def _korona(self, button: discord.ui.button, interaction: discord.MessageInteraction):
        pass


class PrivateRooms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voices = {}
        self.msg_id = int

    @commands.Cog.listener()
    async def on_ready(self):
        for channel in self.bot.get_channel(970754539269537865).channels:
            if channel.id not in [970754640557781073, 970754539751886939]:
                logger.info("Auto-deleting: %s" % channel.name)
                await channel.delete()
        channel = self.bot.get_channel(970754640557781073)
        await channel.purge()
        embed = discord.Embed(
            title="Управление приватной комнатой",
            description="Жми следующие кнопки,чтобы управлять приватной комнатой",
            colour=0x2f3136
        )
        embed.description += """\n
            🖊 - изменить название комнаты
            👥 - изменить кол-во слотов
            🔒 - закрыть комнату для всех
            🔓 - закрыть комнату для всех
            🚪 - выгнать пользователя с комнаты
            ✔ - дать доступ пользователю в комнату
            ❌ - забрать доступ пользователю в комнату
            🔉 - размутить пользователя
            🔇 - замутить пользователя
            👑 - передать владение комнатой
        """
        msg = await channel.send(embed=embed, view=Buttons())
        self.msg_id = msg.id

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.id == 970754539751886939:
            channel = await member.guild.create_voice_channel(
                name=f"Комната %s" % member.display_name,
                category=after.channel.category
            )
            await member.move_to(channel=channel)
            self.voices[channel.id] = member.id
        if before.channel and before.channel.id in self.voices and not len(before.channel.members):
            await before.channel.delete()
            del self.voices[before.channel.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 970754640557781073 and message.author.id != self.bot.user.id:
            await message.delete()

    @commands.Cog.listener()
    async def on_button_click(self, interaction: discord.MessageInteraction):
        if interaction.message.id != self.msg_id:
            return
        if not interaction.author.voice:
            return await interaction.response.send_message(
                "Воу-воу, полегче, зайди в голосовой канал",
                ephemeral=True
            )
        member = interaction.guild.get_member(interaction.author.id)
        channel = member.voice.channel
        if member.id == self.voices[channel.id]:
            await interaction.response.send_message(texts[interaction.component.emoji.name]["start"], ephemeral=True)
            if interaction.component.emoji.name == "🖊️":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                await channel.edit(name=msg.content)
            elif interaction.component.emoji.name == "👥":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if msg.content.isdigit():
                    await channel.edit(user_limit=int(msg.content))
            elif interaction.component.emoji.name == "🔒":
                await channel.set_permissions(
                    interaction.guild.default_role,
                    connect=False
                )
            elif interaction.component.emoji.name == "🔓":
                await channel.set_permissions(
                    interaction.guild.default_role,
                    connect=True
                )
            elif interaction.component.emoji.name == "🚪":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        if u.voice.channel == channel:
                            await u.move_to(channel=None)
            elif interaction.component.emoji.name == "✔":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            connect=True
                        )
            elif interaction.component.emoji.name == "❌":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            connect=False
                        )
            elif interaction.component.emoji.name == "🔉":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            speak=True
                        )
            elif interaction.component.emoji.name == "🔇":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            speak=False
                        )
            elif interaction.component.emoji.name == "👑":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    self.voices[channel.id] = msg.mentions[0].id
            else:
                return await interaction.followup.send(texts[interaction.component.emoji.name]["end"], ephemeral=True)
        else:
            return await interaction.response.send_message(
                "Прости, похоже, что ты не можешь настраивать этот канал :(",
                ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(PrivateRooms(bot))
