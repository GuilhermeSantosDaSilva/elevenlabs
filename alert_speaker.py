"""
secops-voice-alerts
-------------------
Convert security-operations incident alerts into spoken audio (PT-BR)
using the ElevenLabs Text to Speech API.

Usage:
  1. Copy .env.example to .env and add your ELEVENLABS_API_KEY
  2. pip install -r requirements.txt
  3. python alert_speaker.py                 -> converts the sample alerts
     python alert_speaker.py "Custom alert"  -> converts your own text
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
MODEL_ID = "eleven_v3"
OUTPUT_FORMAT = "mp3_44100_128"
OUTPUT_DIR = Path("output")
SAMPLE_ALERTS = [
    "Alerta crítico: câmera 47 offline na estação Sé. Falha de conexão ONVIF detectada às 14 horas e 32 minutos.",
    "Atenção: detecção de objeto abandonado na plataforma 2 do Terminal 3. Analítico de vídeo com confiança de 94 por cento.",
    "Aviso: o servidor de gravação número 5 atingiu 90 por cento da capacidade de armazenamento. Verifique a política de retenção do VMS.",
]


def speak_alert(client: ElevenLabs, text: str, index: int) -> None:
    """Convert one alert to speech, saving the audio and printing metrics."""
    print(f'\n[{index}] Converting: "{text[:60]}..."' if len(text) > 60
          else f'\n[{index}] Converting: "{text}"')

    start = time.perf_counter()

    response = client.text_to_speech.with_raw_response.convert(
        text=text,
        voice_id=VOICE_ID,
        model_id=MODEL_ID,
        output_format=OUTPUT_FORMAT,
    )

    audio_bytes = b"".join(response.data)
    elapsed = time.perf_counter() - start

    out_path = OUTPUT_DIR / f"alert_{index:02d}.mp3"
    out_path.write_bytes(audio_bytes)

    char_cost = response.headers.get("character-cost", "n/a")
    request_id = response.headers.get("request-id", "n/a")

    print(f"    saved      : {out_path}")
    print(f"    latency    : {elapsed:.2f}s for {len(text)} characters")
    print(f"    char cost  : {char_cost}")
    print(f"    request id : {request_id}")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("Missing ELEVENLABS_API_KEY. Copy .env.example to .env and add your key.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    client = ElevenLabs(api_key=api_key)

    alerts = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else SAMPLE_ALERTS

    print(f"Voice: {VOICE_ID} | Model: {MODEL_ID} | Format: {OUTPUT_FORMAT}")
    for i, alert in enumerate(alerts, start=1):
        speak_alert(client, alert, i)

    print(f"\nDone. Audio files are in ./{OUTPUT_DIR}/ — listen and compare voices/models.")


if __name__ == "__main__":
    main()
