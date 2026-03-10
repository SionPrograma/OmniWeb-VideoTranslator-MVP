from .downloader import Downloader
from .audio_converter import AudioConverter
from .transcriber import Transcriber
from .translator import Translator
from .tts_generator import TTSGenerator
from .audio_merger import AudioMerger
from .subtitle_generator import SubtitleGenerator
from .job_manager import job_manager
from ..config import settings
from ..utils.file_utils import get_job_dir, clean_temp_files
import os
import shutil
from pathlib import Path

class ProcessingService:
    def __init__(self):
        self.transcriber = Transcriber()
        self.translator = Translator()
        self.tts = TTSGenerator()

    async def run_pipeline(self, job_id: str, url: str = None, file_path: Path = None, target_lang: str = "es"):
        try:
            # 0. Ensure Directories Exist
            settings.create_directories()
            
            # 1. Acquire Source
            job_manager.update_job(job_id, "preparation", 5, "Initializing workspace...")
            job_dir = get_job_dir(settings.TEMP_DIR, job_id)
            
            if url:
                job_manager.update_job(job_id, "downloading", 10, "Downloading from YouTube...")
                video_path = Downloader.download_youtube(url, job_dir, job_id)
            else:
                video_path = file_path
            
            if not video_path:
                raise Exception("Failed to acquire video source. Check URL or file format.")

            if not video_path.exists():
                raise Exception(f"Video file not found at {video_path}")

            # 2. Extract Audio
            job_manager.update_job(job_id, "audio_extraction", 20, "Extracting audio for analysis...")
            original_audio = AudioConverter.extract_audio(video_path, job_id)

            # 3. Transcribe
            job_manager.update_job(job_id, "transcribing", 40, "Transcribing with Whisper (AI)...")
            transcript_data = self.transcriber.transcribe(original_audio)
            segments = transcript_data.get('segments', [])
            
            # 4. Translate per segment (for sync)
            job_manager.update_job(job_id, "translating", 60.0, f"Translating segments to {target_lang}...")
            
            translated_segments = []
            full_translated_text = []
            
            num_segments = len(segments)
            for i, segment in enumerate(segments):
                # Update progress within stage (Avoid div by zero if num_segments is 0)
                sub_percent = 60.0 + ((i + 1) / num_segments) * 10.0 if num_segments > 0 else 70.0
                job_manager.update_job(job_id, "translating", round(float(sub_percent), 1), f"Translating segment {i+1}/{num_segments}...")
                
                translated_text = self.translator.translate(segment['text'], target_lang)
                segment['translated_text'] = translated_text
                translated_segments.append(segment)
                full_translated_text.append(translated_text)

            # Save full transcript data
            with open(settings.TRANSCRIPT_OUTPUT / f"{job_id}.json", "w", encoding="utf-8") as f:
                import json
                json.dump(transcript_data, f, indent=2)

            with open(settings.TRANSLATION_OUTPUT / f"{job_id}.txt", "w", encoding="utf-8") as f:
                f.write(" ".join(full_translated_text))

            # 5. Generate Dubbing (TTS)
            job_manager.update_job(job_id, "synthesizing", 80.0, "Generating AI voice (Cloning original)...")
            dub_audio_path = settings.AUDIO_OUTPUT / f"{job_id}_dub.wav"
            self.tts.generate(
                " ".join(full_translated_text), 
                dub_audio_path, 
                speaker_wav=original_audio, 
                language=target_lang
            )

            # 6. Generate Subtitles
            job_manager.update_job(job_id, "subtitles", 90.0, "Creating synchronized subtitles...")
            SubtitleGenerator.create_srt(segments, settings.SUBTITLE_OUTPUT / f"{job_id}.srt", use_translated=True)

            # 7. Merge into final video
            job_manager.update_job(job_id, "merging", 95.0, "Merging audio and video tracks...")
            final_video_name = f"{job_id}_final.mp4"
            final_video_path = settings.MERGED_OUTPUT / final_video_name
            AudioMerger.merge_audio_with_original(str(video_path), str(dub_audio_path), str(final_video_path))

            # 8. Complete
            result_url = f"/outputs/merged/{final_video_name}"
            job_manager.update_job(job_id, "complete", 100.0, "Processing complete!", result_url=result_url)
            
            # Cleanup
            clean_temp_files(job_id)

        except Exception as e:
            # Avoid direct access to job_manager.jobs
            current_job = job_manager.get_job(job_id)
            current_percent = current_job["percent"] if current_job else 0.0
            job_manager.update_job(job_id, "failed", current_percent, str(e), error=str(e))

processing_service = ProcessingService()
