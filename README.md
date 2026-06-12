# secops-voice-alerts

Turn security-operations incident alerts into spoken audio (PT-BR) using the
[ElevenLabs Text to Speech API](https://elevenlabs.io/docs/eleven-api/quickstart).

## What it does

- Converts incident alerts (sample PT-BR alerts included, or your own text) to MP3
- Measures **end-to-end latency** per request
- Reads **character cost** and **request id** from the response headers, as shown
  in the [API reference introduction](https://elevenlabs.io/docs/api-reference/introduction)
- Saves audio to `./output/` so different voices/models can be compared side by side

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your ELEVENLABS_API_KEY
```

Get an API key at https://elevenlabs.io/app/settings/api-keys (free tier works).

## Run

```bash
python alert_speaker.py                          # converts the 3 sample alerts
python alert_speaker.py "Alerta: porta aberta no datacenter 2."   # custom alert
```

Example output:

```
[1] Converting: "Alerta crítico: câmera 47 offline na estação Sé..."
    saved      : output/alert_01.mp3
    latency    : X.XXs for 109 characters
    char cost  : XXX
    request id : ...
```

## Notes & observations

<!-- TODO(me): fill in after running -->
- How PT-BR voices handle technical vocabulary (ONVIF, VMS, camera IDs):
- Latency observed and what it means for real-time operator alerts:
- Voices compared and which sounded most natural for alerts:
- Docs friction / things that surprised me:

## Next steps

- Stream audio instead of waiting for the full file
  ([streaming guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/streaming))
  to cut perceived latency for live alerts
- Hook this to a real event source (webhook from a VMS analytics pipeline)
- Explore ElevenAgents for two-way voice: operator asks "status da câmera 47?"
  and the agent answers from a knowledge base
