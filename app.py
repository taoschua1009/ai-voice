import base64
import os
import tempfile

from fastapi import FastAPI
from pydantic import BaseModel

from asr import ASRService
from enhance import enhance_with_demucs

app = FastAPI()
asr = ASRService(
    model_size=os.getenv("WHISPER_MODEL", "small"),
    device=os.getenv("WHISPER_DEVICE", "cpu"),
    compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
)

class TranscribeRequest(BaseModel):
    audio_base64: str
    mime_type: str = "audio/webm"
    enhance: bool = True

@app.post("/transcribe")
def transcribe(req: TranscribeRequest):
    suffix = ".webm" if "webm" in req.mime_type else ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(base64.b64decode(req.audio_base64))
        input_path = f.name

    target_path = input_path
    if req.enhance:
        try:
            target_path = enhance_with_demucs(input_path)
        except Exception:
            target_path = input_path

    text = asr.transcribe_file(target_path)
    return {"text": text}