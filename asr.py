from faster_whisper import WhisperModel

class ASRService:
    def __init__(self, model_size: str = "small", device: str = "cpu", compute_type: str = "int8"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe_file(self, path: str) -> str:
        segments, _ = self.model.transcribe(path, vad_filter=True)
        parts = [seg.text.strip() for seg in segments if seg.text.strip()]
        return " ".join(parts).strip()