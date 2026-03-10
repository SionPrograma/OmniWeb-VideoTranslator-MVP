# System Architecture

## Overview
The VideoTranslator follows a **Modular Service-Oriented Architecture (SOA)** within a FastAPI monolith. This allows each stage of the translation pipeline to be improved or replaced independently.

## Data Flow
1. **Request Intake**: `process.py` receives a URL or UploadFile.
2. **Job Initiation**: `JobManager` creates a unique `job_id` and starts a `BackgroundTasks` thread.
3. **Download/Prep**: `Downloader` fetches the media to a temp directory.
4. **Extraction**: `AudioConverter` uses FFmpeg to isolate audio.
5. **Transcription**: `Whisper` converts audio to text (JSON).
6. **Translation**: `LibreTranslate` translates text to target language.
7. **Synthesis**: `Coqui TTS` generates a new WAV file.
8. **Finalization**: Result URL is served via `/outputs` static mount.

## Key Design Principles
- **Asynchronicity**: Long-running AI tasks don't block the API.
- **Stateless API**: Results are stored on disk, state is in-memory (extensible to Redis/SQL).
- **Separation of Concerns**: UI, API, and Engine are decoupled.
