from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pptx import Presentation
from openai import OpenAI
import tempfile
import os

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.stratumadmissions.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SongRequest(BaseModel):
    lyrics: str
    title: str
    artist: str

@app.post("/generate")
async def generate_ppt(data: SongRequest):

    # Create presentation from template
    prs = Presentation("Working Template.pptx")

    # Basic example – replace with your full duplication logic
    slide = prs.slides[0]
    slide.shapes.title.text = data.title

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    prs.save(temp_file.name)

    return FileResponse(
        temp_file.name,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"{data.title}.pptx"
    )
    
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
