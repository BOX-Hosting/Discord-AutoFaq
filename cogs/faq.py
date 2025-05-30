import discord
from discord.ext import commands
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vectorizer = TfidfVectorizer()
        self.load_faq()
        if config.ENABLE_HIDE_BUTTON:
            self.bot.add_view(HideView())

    def load_faq(self):
        with open("data.json", "r", encoding="utf-8") as f:
            self.faq_data = json.load(f)
        self.questions = [item["question"].lower() for item in self.faq_data]
        self.embeddings = self.vectorizer.fit_transform(self.questions)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id not in config.ALLOWED_CHANNEL_IDS:
            return
        if not message.content.strip():
            return

        user_input = message.content.lower()
        user_embedding = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_embedding, self.embeddings)[0]
        max_similarity = similarities.max()
        index = similarities.argmax()

        if max_similarity >= config.SIMILARITY_THRESHOLD:
            answer = self.faq_data[index]["answer"]

            if config.ENABLE_HIDE_BUTTON:
                embed = discord.Embed(
                    title="🔍 Ответ на ваш вопрос",
                    description=answer,
                    color=discord.Color.blurple()
                )
                view = HideView(author_id=message.author.id)
                await message.reply(embed=embed, view=view, mention_author=False)
            else:
                await message.reply(content=answer, mention_author=False)


class HideView(discord.ui.View):
    def __init__(self, author_id: int = None):
        super().__init__(timeout=None)
        if author_id:
            self.children[0].custom_id = f"hide_button:{author_id}"

    @discord.ui.button(label="Скрыть ответ", style=discord.ButtonStyle.danger, custom_id="hide_button:0")
    async def hide_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            _, author_id = button.custom_id.split(":")
            author_id = int(author_id)
        except:
            await interaction.response.send_message("Ошибка при проверке доступа.", ephemeral=True)
            return

        user_id = interaction.user.id
        has_privilege = any(role.id in config.CAN_HIDE_FOREIGN_MESSAGES_ROLE_IDS for role in interaction.user.roles)

        if user_id != author_id and not has_privilege:
            await interaction.response.send_message("Вы не можете скрыть этот ответ.", ephemeral=True)
            return

        await interaction.message.delete()


async def setup(bot):
    await bot.add_cog(FAQ(bot))
