# AI Image Generation Agent 🎨

A powerful and flexible Python-based AI agent for generating images from text prompts. Supports multiple AI backends including Hugging Face Diffusers (Stable Diffusion), OpenAI DALL-E, and Stability AI.

## Features ✨

- **Multiple AI Backends**: Choose from Hugging Face, OpenAI, or Stability AI
- **Easy CLI Interface**: Simple command-line interface for quick image generation
- **Flexible Configuration**: Customize models, parameters, and output settings
- **Batch Generation**: Generate multiple images at once
- **Reproducible Results**: Use seeds for consistent outputs
- **Metadata Support**: Save prompts and settings with generated images
- **Memory Optimized**: Efficient memory usage for GPU and CPU generation

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster generation

### Basic Installation

```bash
# Clone or download the repository
cd /path/to/image-generation-agent

# Install dependencies
pip install -r requirements.txt
```

### Backend-Specific Setup

#### Hugging Face (Default - No API Key Required)

```bash
# Install core dependencies
pip install torch diffusers transformers accelerate pillow

# For faster generation on NVIDIA GPUs (optional)
pip install xformers
```

#### OpenAI DALL-E

```bash
# Install OpenAI library
pip install openai

# Set your API key
export OPENAI_API_KEY='your-api-key-here'
```

Get your API key from: https://platform.openai.com/api-keys

#### Stability AI

```bash
# Install Stability SDK
pip install stability-sdk

# Set your API key
export STABILITY_API_KEY='your-api-key-here'
```

Get your API key from: https://platform.stability.ai/

## Quick Start 🎯

### Basic Usage

Generate a single image with default settings:

```bash
python image_generation_agent.py "a beautiful sunset over mountains"
```

### Specify Backend

```bash
# Use Hugging Face (default)
python image_generation_agent.py "a cat wearing sunglasses" --backend huggingface

# Use OpenAI DALL-E
python image_generation_agent.py "a futuristic city" --backend openai

# Use Stability AI
python image_generation_agent.py "abstract art" --backend stability
```

### Advanced Options

```bash
python image_generation_agent.py \
  "a majestic dragon flying over a castle" \
  --backend huggingface \
  --width 768 \
  --height 768 \
  --num-images 4 \
  --steps 50 \
  --guidance-scale 7.5 \
  --negative-prompt "blurry, low quality, distorted" \
  --seed 42 \
  --output-dir my_images \
  --prefix dragon
```

## Command-Line Options 📋

| Option | Description | Default |
|--------|-------------|---------|
| `prompt` | Text description of image (required) | - |
| `--backend` | AI backend (huggingface/openai/stability) | huggingface |
| `--model` | Specific model to use | Backend default |
| `--negative-prompt` | Things to avoid in image | None |
| `--width` | Image width in pixels | 512 |
| `--height` | Image height in pixels | 512 |
| `--num-images` | Number of images to generate | 1 |
| `--steps` | Number of inference steps | 50 |
| `--guidance-scale` | How closely to follow prompt (1-20) | 7.5 |
| `--seed` | Random seed for reproducibility | Random |
| `--output-dir` | Output directory | generated_images |
| `--prefix` | Filename prefix | image |

## Configuration Management ⚙️

### Create Configuration File

```bash
python config.py
```

This creates a sample configuration file `image_agent_config.json`:

```json
{
  "backend": "huggingface",
  "models": {
    "huggingface": "stabilityai/stable-diffusion-2-1",
    "openai": "dall-e-3",
    "stability": "stable-diffusion-xl-1024-v1-0"
  },
  "generation": {
    "width": 768,
    "height": 768,
    "num_images": 1,
    "num_inference_steps": 50,
    "guidance_scale": 7.5,
    "negative_prompt": "blurry, low quality, distorted"
  },
  "output": {
    "directory": "generated_images",
    "prefix": "ai_art",
    "format": "png"
  }
}
```

### Using Configuration in Code

```python
from config import Config

config = Config('image_agent_config.json')
config.print_config()

# Get values
backend = config.get('backend')
width = config.get('generation.width')

# Set values
config.set('generation.width', 1024)
config.save()
```

## Available Models 🤖

### Hugging Face Models

- `stabilityai/stable-diffusion-2-1` (default)
- `stabilityai/stable-diffusion-xl-base-1.0`
- `runwayml/stable-diffusion-v1-5`
- `CompVis/stable-diffusion-v1-4`
- `prompthero/openjourney`
- `dreamlike-art/dreamlike-photoreal-2.0`

### OpenAI Models

- `dall-e-3` (default, highest quality)
- `dall-e-2`

### Stability AI Models

- `stable-diffusion-xl-1024-v1-0` (default)
- `stable-diffusion-v1-6`

## Usage Examples 💡

### Example 1: High-Quality Portrait

```bash
python image_generation_agent.py \
  "professional portrait photo of a woman, studio lighting, 8k, detailed" \
  --width 768 \
  --height 768 \
  --steps 75 \
  --guidance-scale 8.0 \
  --negative-prompt "cartoon, anime, illustration, low quality"
```

### Example 2: Artistic Style

```bash
python image_generation_agent.py \
  "oil painting of a serene lake at dawn, impressionist style" \
  --model "prompthero/openjourney" \
  --width 512 \
  --height 512 \
  --guidance-scale 9.0
```

### Example 3: Batch Generation

```bash
python image_generation_agent.py \
  "cute robot character design, multiple angles" \
  --num-images 8 \
  --seed 12345 \
  --output-dir robot_designs
```

### Example 4: Using OpenAI DALL-E

```bash
export OPENAI_API_KEY='your-key'
python image_generation_agent.py \
  "a photorealistic image of a futuristic car" \
  --backend openai \
  --width 1024 \
  --height 1024
```

## Python API Usage 🐍

You can also use the agent programmatically:

```python
from image_generation_agent import ImageGenerationAgent

# Initialize agent
agent = ImageGenerationAgent(backend='huggingface')

# Generate images
images = agent.generate(
    prompt="a magical forest with glowing mushrooms",
    negative_prompt="dark, scary",
    width=768,
    height=768,
    num_images=2,
    num_inference_steps=50,
    guidance_scale=7.5,
    seed=42
)

# Save images
saved_paths = agent.save_images(
    images=images,
    output_dir="my_images",
    prefix="forest",
    prompt="a magical forest with glowing mushrooms"
)

print(f"Generated {len(saved_paths)} images")
```

## Tips for Better Results 💎

### Prompt Engineering

1. **Be Specific**: Include details about style, lighting, composition
   - ❌ "a dog"
   - ✅ "a golden retriever puppy playing in a sunny garden, professional photography"

2. **Use Quality Modifiers**: Add terms like "high quality", "detailed", "8k", "professional"

3. **Specify Art Style**: "oil painting", "digital art", "photorealistic", "anime style"

4. **Use Negative Prompts**: Exclude unwanted elements
   - "blurry, low quality, distorted, watermark, text"

### Parameter Tuning

- **Guidance Scale**: 
  - Lower (5-7): More creative, less literal
  - Higher (8-15): More literal, follows prompt closely
  
- **Inference Steps**:
  - Fewer (20-30): Faster, less detailed
  - More (50-100): Slower, more refined

- **Image Size**:
  - 512x512: Fast, good for testing
  - 768x768: Balanced quality/speed
  - 1024x1024: High quality, slower

## Troubleshooting 🔧

### Out of Memory Error

```bash
# Reduce image size
--width 512 --height 512

# Generate fewer images at once
--num-images 1

# Use CPU instead of GPU (slower)
export CUDA_VISIBLE_DEVICES=""
```

### Model Download Issues

```bash
# Set Hugging Face cache directory
export HF_HOME="/path/to/cache"

# Use Hugging Face token for gated models
export HF_TOKEN="your-token"
```

### API Rate Limits

For OpenAI and Stability AI, be aware of rate limits:
- Add delays between requests
- Use batch generation wisely
- Check your API usage dashboard

## Performance Optimization ⚡

### GPU Acceleration

```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Monitor GPU usage
nvidia-smi -l 1
```

### Memory Optimization

The agent automatically enables:
- Attention slicing for lower memory usage
- Mixed precision (FP16) on GPU
- Efficient scheduler (DPM-Solver)

## Project Structure 📁

```
.
├── image_generation_agent.py  # Main agent with CLI
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── IMAGE_AGENT_README.md      # This file
├── example_usage.py           # Usage examples
└── generated_images/          # Output directory (created automatically)
```

## Contributing 🤝

Contributions are welcome! Areas for improvement:
- Additional backend support (Midjourney API, etc.)
- Image-to-image generation
- Inpainting and outpainting
- LoRA model support
- Web UI interface
- Batch processing from file

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- [Stability AI](https://stability.ai/) for Stable Diffusion
- [Hugging Face](https://huggingface.co/) for the Diffusers library
- [OpenAI](https://openai.com/) for DALL-E
- The open-source AI community

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example usage scripts

---

**Happy Creating! 🎨✨**
