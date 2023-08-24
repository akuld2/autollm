import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import pandas as pd
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from random_word import RandomWords

r = RandomWords()

cookies = json.loads(open("bing_cookies_*.json", encoding="utf-8").read())
num_bots = 10 #200
num_queries_per_bot = 20

async def initialize_bot(bot):
    for i in tqdm(range(3), desc="Initializing bot", leave=False):
        response = await bot.ask(prompt="write a long 5 paragraph essay explaining what this word means in 1000 words " + r.get_random_word(), conversation_style=ConversationStyle.precise, simplify_response=True)
        text = response["text"]
        time.sleep(1)

async def main():
    for i in tqdm(range(num_bots), desc="Bots created"):
        cookies = json.loads(open("bing_cookies_*.json", encoding="utf-8").read())
        bot = await Chatbot.create(cookies=cookies)
        await initialize_bot(bot)
        for j in tqdm(range(num_queries_per_bot), desc="Generating code snippets", leave=False):
            response = await bot.ask(prompt="Generate a short random Python code problem. make it unique. Then, solve that problem.", conversation_style=ConversationStyle.precise, simplify_response=True)
            text = response["text"]
            with open(f"out/responses{i}.txt", "a") as f:
                f.write("-----------------\n")
                f.write(text)
            time.sleep(1)

asyncio.run(main())