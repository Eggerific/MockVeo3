from dataclasses import dataclass
from typing import List, Dict, Optional
import re
import yaml
from pathlib import Path

@dataclass
class Scene:
    scene_description: str
    duration_seconds: float
    characters: List[str]
    camera_motion: str
    visual_style: str
    audio_instruction: Optional[str]
    transition_to_next: str

class PromptParser:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.default_duration = self.config['video']['default_duration']
        self.default_style = self.config['video']['default_style']
        self.default_transition = self.config['transitions']['default']

    def _extract_characters(self, text: str) -> List[str]:
        # Simple character extraction - can be enhanced with NLP
        # This is a placeholder implementation
        words = text.split()
        potential_chars = [word for word in words if word[0].isupper()]
        return list(set(potential_chars))

    def _infer_camera_motion(self, text: str) -> str:
        # Simple camera motion inference - can be enhanced
        if "walk" in text.lower() or "move" in text.lower():
            return "tracking"
        elif "battle" in text.lower() or "fight" in text.lower():
            return "dynamic"
        return "static"

    def parse_prompt(self, prompt: str) -> List[Scene]:
        # Split prompt into scenes using common transition words
        transition_words = ["then", "after", "next", "later", "finally"]
        scene_texts = re.split(f"({'|'.join(transition_words)})", prompt)
        
        scenes = []
        for i in range(0, len(scene_texts), 2):
            if i + 1 < len(scene_texts):
                scene_text = scene_texts[i].strip()
                transition = scene_texts[i + 1].strip()
            else:
                scene_text = scene_texts[i].strip()
                transition = self.default_transition

            scene = Scene(
                scene_description=scene_text,
                duration_seconds=self.default_duration,
                characters=self._extract_characters(scene_text),
                camera_motion=self._infer_camera_motion(scene_text),
                visual_style=self.default_style,
                audio_instruction=None,  # Can be enhanced with audio inference
                transition_to_next=transition
            )
            scenes.append(scene)

        return scenes

    def export_scenes(self, scenes: List[Scene], output_path: str) -> None:
        """Export scene metadata to JSON file"""
        import json
        scenes_dict = [vars(scene) for scene in scenes]
        with open(output_path, 'w') as f:
            json.dump(scenes_dict, f, indent=2) 