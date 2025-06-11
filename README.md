# MockVeo3 - AI Video Generation Framework

A modular Python framework for AI-powered video generation, inspired by Google Veo (v3). This project simulates a pipeline that breaks down creative prompts into scene-based instructions and generates videos with checkpoint-based control.

## Features

- Prompt parsing into structured scenes
- Scene-based video generation with metadata
- Configurable transitions and effects
- Audio track support
- Progress logging and checkpointing
- Export of scene metadata

## Project Structure

```
MockVeo3/
├── src/
│   ├── main.py              # Main entry point
│   ├── prompt_parser.py     # Prompt parsing and scene structuring
│   ├── scene_generator.py   # Video clip generation
│   └── video_editor.py      # Video composition and effects
├── output/                  # Generated videos and metadata
├── config.yaml             # Configuration settings
└── requirements.txt        # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MockVeo3.git
cd MockVeo3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the video generation pipeline with a creative prompt:

```bash
python src/main.py --prompt "Zeus walks through Mount Olympus as clouds roll in, then battles Poseidon in a stormy sea"
```

Optional arguments:
- `--config`: Path to config file (default: config.yaml)
- `--output`: Output video path (default: output/final_video.mp4)

## Configuration

The `config.yaml` file contains settings for:
- Video resolution and frame rate
- Default scene duration and style
- Transition effects
- Audio settings
- Output paths
- Logging configuration

## Development

### Adding New Features

1. Scene Generation:
   - Extend `DummyVideoGen` class in `scene_generator.py`
   - Implement custom frame generation logic

2. Transitions:
   - Add new transition types in `video_editor.py`
   - Update config.yaml with new transition settings

3. Audio:
   - Implement audio generation in `scene_generator.py`
   - Add audio processing in `video_editor.py`

### Testing

Run the example prompt:
```bash
python src/main.py --prompt "A peaceful forest scene, then a dramatic mountain view"
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 