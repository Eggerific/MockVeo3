import argparse
import logging
from pathlib import Path
import yaml
from prompt_parser import PromptParser
from scene_generator import SceneGenerator
from video_editor import VideoEditor

def setup_logging(config):
    logging.basicConfig(
        level=config['logging']['level'],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='AI Video Generation Framework')
    parser.add_argument('--prompt', type=str, required=True, help='Creative prompt for video generation')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--output', type=str, default='output/final_video.mp4', help='Output video path')
    args = parser.parse_args()

    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    logger = setup_logging(config)
    logger.info("Starting video generation pipeline")

    # Initialize components
    prompt_parser = PromptParser(args.config)
    scene_generator = SceneGenerator(args.config)
    video_editor = VideoEditor(args.config)

    try:
        # Parse prompt into scenes
        logger.info("Parsing prompt into scenes")
        scenes = prompt_parser.parse_prompt(args.prompt)
        logger.info(f"Parsed {len(scenes)} scenes")

        # Export scene metadata
        metadata_path = Path(config['output']['directory']) / 'scene_metadata.json'
        prompt_parser.export_scenes(scenes, str(metadata_path))
        logger.info(f"Exported scene metadata to {metadata_path}")

        # Generate video clips for each scene
        logger.info("Generating video clips")
        scene_clips = scene_generator.generate_all_scenes(scenes)
        logger.info("Video clip generation completed")

        # Compose final video
        logger.info("Composing final video")
        final_video_path = video_editor.compose_video(scene_clips, args.output)
        logger.info(f"Final video saved to {final_video_path}")

    except Exception as e:
        logger.error(f"Error during video generation: {str(e)}")
        raise

if __name__ == "__main__":
    main() 