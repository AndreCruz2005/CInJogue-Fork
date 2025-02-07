from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gemini import GeminiModel
from giantbomb import search_game
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5000",
    "http://192.168.56.1:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bot = GeminiModel()


@app.get("/genai/{prompt}")
async def test(prompt: str):
    reply = eval(bot.send_message(prompt))
    for comamnd in reply:
        titles = comamnd.get('titles', [])
    response = search_game(titles[0] if titles else "Fortnite")
    return response
    

    