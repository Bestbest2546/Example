from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_gpt(message: str) -> dict:
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": message}],
        )

        response_text = completion.choices[0].message.content if completion.choices else ""

        return {"return": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))