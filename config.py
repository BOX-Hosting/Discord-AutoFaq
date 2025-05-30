import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SIMILARITY_THRESHOLD = 0.75 #Чувствительность

STATUS = os.getenv("STATUS", "dnd").lower()  
# online - в сети
#idle - неактивен
#dnd - не беспокоить
#invisible - невидимый

STATUS_TEXT = os.getenv("STATUS_TEXT", "Сижу отвечаю на воспосы 💭")  # Текст активности