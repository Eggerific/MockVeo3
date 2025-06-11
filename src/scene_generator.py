import cv2
import numpy as np
from pathlib import Path
import yaml
import logging
from typing import Dict, Optional
from .prompt_parser import Scene

class DummyVideoGen:
    """Mock video generator that creates placeholder videos"""
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.resolution = tuple(self.config['video']['output_resolution'])
        self.fps = self.config['video']['frame_rate']
        
        # Set up logging
        logging.basicConfig(level=self.config['logging']['level'])
        self.logger = logging.getLogger(__name__)

    def _create_placeholder_frame(self, scene: Scene, frame_num: int) -> np.ndarray:
        """Create a placeholder frame with scene information"""
        frame = np.zeros((*self.resolution[::-1], 3), dtype=np.uint8)
        
        # Add some visual elements based on scene description
        color = (frame_num % 255, (frame_num + 85) % 255, (frame_num + 170) % 255)
        cv2.rectangle(frame, (100, 100), (self.resolution[0]-100, self.resolution[1]-100), color, -1)
        
        # Add text overlay
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, scene.scene_description[:50], (150, 150), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Style: {scene.visual_style}", (150, 200), font, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Camera: {scene.camera_motion}", (150, 250), font, 0.7, (255, 255, 255), 2)
        
        return frame

    def generate_clip(self, scene: Scene, output_path: Optional[str] = None) -> str:
        """Generate a video clip for the given scene"""
        if output_path is None:
            output_path = Path(self.config['output']['temp_directory']) / f"scene_{hash(scene.scene_description)}.mp4"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Generating clip for scene: {scene.scene_description}")
        
        # Calculate total frames
        total_frames = int(scene.duration_seconds * self.fps)
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, self.fps, self.resolution)
        
        # Generate frames
        for frame_num in range(total_frames):
            frame = self._create_placeholder_frame(scene, frame_num)
            out.write(frame)
            
            # Log progress
            if frame_num % self.fps == 0:
                self.logger.info(f"Generated {frame_num}/{total_frames} frames")
        
        out.release()
        self.logger.info(f"Clip generated and saved to {output_path}")
        
        return str(output_path)

class SceneGenerator:
    def __init__(self, config_path: str = "config.yaml"):
        self.video_gen = DummyVideoGen(config_path)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Set up logging
        logging.basicConfig(level=self.config['logging']['level'])
        self.logger = logging.getLogger(__name__)

    def generate_all_scenes(self, scenes: list[Scene]) -> Dict[str, str]:
        """Generate video clips for all scenes"""
        scene_clips = {}
        
        for i, scene in enumerate(scenes):
            self.logger.info(f"Processing scene {i+1}/{len(scenes)}")
            clip_path = self.video_gen.generate_clip(scene)
            scene_clips[scene.scene_description] = clip_path
            
        return scene_clips 