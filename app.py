from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini-Pro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize the GenerativeModel instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are a healthcare advisor helping diabetic patients with their mental and physical health."
)

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Add a Gemini Chat history object
if "chat" not in globals():
    chat = model.start_chat(history=[])

@app.post("/chat", response_model=ChatResponse)
async def chat_with_model(request: ChatRequest):
    global chat
    prompt = request.message
    response = chat.send_message(prompt)
    return ChatResponse(response=response.text)

if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)