from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx import fadein, fadeout, crossfadein
import yaml
import logging
from pathlib import Path
from typing import Dict, List

class VideoEditor:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.transition_duration = self.config['transitions']['duration']
        self.default_transition = self.config['transitions']['default']
        
        # Set up logging
        logging.basicConfig(level=self.config['logging']['level'])
        self.logger = logging.getLogger(__name__)

    def _apply_transition(self, clip: VideoFileClip, transition_type: str) -> VideoFileClip:
        """Apply transition effect to a clip"""
        if transition_type == "fade":
            return clip.fx(fadein, self.transition_duration).fx(fadeout, self.transition_duration)
        elif transition_type == "dissolve":
            return clip.fx(crossfadein, self.transition_duration)
        else:  # cut or unknown transition
            return clip

    def compose_video(self, scene_clips: Dict[str, str], output_path: str) -> str:
        """Compose final video from scene clips with transitions"""
        self.logger.info("Starting video composition")
        
        # Load all clips
        clips = []
        for scene_desc, clip_path in scene_clips.items():
            clip = VideoFileClip(clip_path)
            clips.append(clip)
        
        # Apply transitions
        processed_clips = []
        for i, clip in enumerate(clips):
            # Apply transition based on scene metadata or default
            transition_type = self.default_transition
            processed_clip = self._apply_transition(clip, transition_type)
            processed_clips.append(processed_clip)
            
            self.logger.info(f"Processed clip {i+1}/{len(clips)}")
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(processed_clips)
        
        # Write final video
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Writing final video to {output_path}")
        final_clip.write_videofile(
            str(output_path),
            fps=self.config['video']['frame_rate'],
            codec='libx264',
            audio_codec='aac'
        )
        
        # Close all clips
        for clip in clips:
            clip.close()
        final_clip.close()
        
        self.logger.info("Video composition completed")
        return str(output_path)

    def add_audio(self, video_path: str, audio_path: str, output_path: str) -> str:
        """Add audio track to the video"""
        self.logger.info("Adding audio track to video")
        
        video = VideoFileClip(video_path)
        audio = VideoFileClip(audio_path).audio
        
        # Set audio volume
        audio = audio.volumex(self.config['audio']['default_volume'])
        
        # Combine video and audio
        final = video.set_audio(audio)
        
        # Write final video
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Writing final video with audio to {output_path}")
        final.write_videofile(
            str(output_path),
            fps=self.config['video']['frame_rate'],
            codec='libx264',
            audio_codec='aac'
        )
        
        # Close clips
        video.close()
        audio.close()
        final.close()
        
        self.logger.info("Audio addition completed")
        return str(output_path) 