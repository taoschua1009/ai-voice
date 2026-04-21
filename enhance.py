import os
import subprocess
import tempfile

def enhance_with_demucs(input_path: str) -> str:
    """
    Optional enhancement stage.
    In production, run only for sufficiently long/noisy clips.
    """
    out_dir = tempfile.mkdtemp(prefix="demucs_")
    cmd = [
        "python", "-m", "demucs.separate",
        "-n", "htdemucs",
        "--two-stems=vocals",
        "-o", out_dir,
        input_path
    ]
    subprocess.run(cmd, check=True)

    base = os.path.splitext(os.path.basename(input_path))[0]
    vocals_path = os.path.join(out_dir, "htdemucs", base, "vocals.wav")
    if not os.path.exists(vocals_path):
      return input_path
    return vocals_path