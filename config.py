import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SIMILARITY_THRESHOLD = 0.75 #Чувствительность

STATUS = os.getenv("STATUS", "online").lower()  
# online - в сети
# idle - неактивен
# dnd - не беспокоить
# invisible - невидимый

ACTIVY = os.getenv("ACTIVY", "online").lower()  
# Game - играет ...
# Stream - Стримит ...
# watching - смотрит ...
# listening - слушает ...

STATUS_TEXT = os.getenv("STATUS_TEXT", "BOX-Hosting.ru")  # Текст активности
STATUS_URLSTREM = os.getenv("STATUS_URLSTREM", "https://www.youtube.com/watch?v=nuHtgzBe_Ho") 