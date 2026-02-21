from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pptx import Presentation
from openai import OpenAI
import tempfile
import os

app = FastAPI()

# ✅ CORS — allow your Squarespace domain
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

    prs = Presentation("Working Template.pptx")

    slide = prs.slides[0]
    slide.shapes.title.text = data.title

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
    prs.save(temp_file.name)

    return FileResponse(
        temp_file.name,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=f"{data.title}.pptx"
    )
