# Project Roadmap 🛣️

## Phase 1: MVP (Completed)
- [x] Basic YouTube download.
- [x] Local Whisper transcription.
- [x] Simple translation integration.
- [x] Basic TTS generation.
- [x] Responsive dark UI.

## Phase 2: Performance & Scalability
- [ ] **Workers & Queues**: Move from threading to Redis/Celery for handling concurrent heavy jobs.
- [ ] **GPU Support**: Enable CUDA for faster Whisper/TTS inference.
- [ ] **Dockerization**: Create a multi-container setup (API, LibreTranslate, Workers).

## Phase 3: Enhanced Features
- [ ] **Video Preview**: Show the original video alongside the translation.
- [ ] **Subtitle Editor**: Allow users to edit the transcript before generating TTS.
- [ ] **Voice Cloning**: Use RVC (Retrieval-based Voice Conversion) to keep the original speaker's tone.
- [ ] **Local File Upload**: Drag-and-drop interface for `.mp4` and `.mov` files.
