# main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from streamlit.server.server import Server as StreamlitServer
import streamlit as st

# Import your Streamlit app
from streamlit_app import main as streamlit_main

app = FastAPI()

# Templates for FastAPI (optional)
templates = Jinja2Templates(directory="templates")

# Route to render Streamlit app
@app.get("/")
async def streamlit_endpoint(request: Request):
    # Function to run Streamlit app
    def run_streamlit_app():
        streamlit_main()

    # Create Streamlit server instance
    streamlit_server = StreamlitServer.run(
        command=run_streamlit_app,
        port=8501,
        allow_websocket_origin=["localhost", "127.0.0.1"]
    )

    return HTMLResponse(content=f"<iframe src='http://localhost:8501/' width=100% height=1000></iframe>", status_code=200)

