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

    def load_faq(self):
        with open("data.json", "r", encoding="utf-8") as f:
            self.faq_data = json.load(f)
        self.questions = [item["question"].lower() for item in self.faq_data]
        self.embeddings = self.vectorizer.fit_transform(self.questions)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.content.strip():
            return
        user_input = message.content.lower()
        user_embedding = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_embedding, self.embeddings)[0]
        max_similarity = similarities.max()
        index = similarities.argmax()
        if max_similarity >= config.SIMILARITY_THRESHOLD:
            answer = self.faq_data[index]["answer"]
            await message.reply(answer)

async def setup(bot):
    await bot.add_cog(FAQ(bot))
