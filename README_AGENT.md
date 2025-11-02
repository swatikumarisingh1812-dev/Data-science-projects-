# AI Image Generator Agent

A flexible Python-based AI agent for generating images from text prompts using multiple backends including Stability AI, OpenAI DALL-E, Hugging Face, and local models.

## Features

- 🎨 **Multiple Backends**: Support for Stability AI, OpenAI DALL-E, Hugging Face Inference API, and local models
- 🔧 **Highly Configurable**: Customize image size, quality, steps, guidance scale, and more
- 🎯 **Negative Prompts**: Specify what you don't want in your images
- 🌱 **Reproducible**: Use seeds for consistent results
- 📦 **Batch Generation**: Generate multiple images from different prompts
- 💾 **Auto-save**: Automatically save images with metadata
- 🔑 **Environment-based Config**: Secure API key management via .env files

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **For local model generation (optional, requires GPU):**

```bash
pip install torch diffusers transformers accelerate
```

4. **For OpenAI DALL-E (optional):**

```bash
pip install openai
```

## Configuration

### API Keys

Create a `.env` file in the project root with your API keys:

```env
# Stability AI (https://platform.stability.ai/)
STABILITY_API_KEY=your_stability_api_key_here

# OpenAI (https://platform.openai.com/)
OPENAI_API_KEY=your_openai_api_key_here

# Hugging Face (https://huggingface.co/settings/tokens) - Optional
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### Getting API Keys

- **Stability AI**: Sign up at [platform.stability.ai](https://platform.stability.ai/) and get your API key
- **OpenAI**: Create an account at [platform.openai.com](https://platform.openai.com/) and generate an API key
- **Hugging Face**: Register at [huggingface.co](https://huggingface.co/) and create a token (optional, but recommended for better rate limits)

## Quick Start

### Basic Usage

```python
from image_generator import ImageGeneratorAgent

# Initialize the agent
agent = ImageGeneratorAgent(backend='stability')

# Generate an image
prompt = "A serene mountain landscape at sunset, digital art"
images = agent.generate(prompt=prompt, width=512, height=512, num_images=1)

# Save the images
agent.save_images(images, prompt=prompt, prefix="mountain")
```

### Check Available Backends

```python
from image_generator import ImageGeneratorAgent

# Check which backends are configured
backends = ImageGeneratorAgent.list_available_backends()
print(backends)
# Output: {'stability': True, 'openai': False, 'huggingface': True, 'local': True}
```

## Usage Examples

### 1. Basic Generation

```python
agent = ImageGeneratorAgent(backend='stability')

images = agent.generate(
    prompt="A cute robot playing with a cat, cartoon style",
    width=512,
    height=512,
    num_images=1
)

agent.save_images(images, prompt="robot and cat")
```

### 2. Using Negative Prompts

```python
agent = ImageGeneratorAgent(backend='stability')

images = agent.generate(
    prompt="A beautiful garden with flowers",
    negative_prompt="dark, gloomy, dead plants, winter",
    width=512,
    height=512,
    guidance_scale=8.0
)
```

### 3. Batch Generation

```python
agent = ImageGeneratorAgent(backend='stability')

prompts = [
    "A futuristic city with flying cars",
    "A peaceful zen garden",
    "An underwater coral reef"
]

results = agent.batch_generate(prompts=prompts, width=512, height=512)

for prompt, images in results.items():
    agent.save_images(images, prompt=prompt)
```

### 4. Reproducible Results with Seeds

```python
agent = ImageGeneratorAgent(backend='stability')

# Generate the same image multiple times
images = agent.generate(
    prompt="A steampunk airship",
    seed=42,
    num_images=1
)
```

### 5. Using Different Backends

```python
# Stability AI
agent_stability = ImageGeneratorAgent(backend='stability')

# OpenAI DALL-E
agent_openai = ImageGeneratorAgent(backend='openai', model='dall-e-3')

# Hugging Face
agent_hf = ImageGeneratorAgent(
    backend='huggingface',
    model='stabilityai/stable-diffusion-2-1'
)

# Local model (requires GPU)
agent_local = ImageGeneratorAgent(
    backend='local',
    model='runwayml/stable-diffusion-v1-5'
)
```

### 6. Advanced Parameters

```python
agent = ImageGeneratorAgent(backend='stability')

images = agent.generate(
    prompt="A magical forest with glowing mushrooms",
    negative_prompt="dark, scary",
    width=768,
    height=768,
    num_images=2,
    steps=50,              # More steps = higher quality (but slower)
    guidance_scale=9.0,    # Higher = follows prompt more closely
    seed=12345
)
```

## Available Models

### Stability AI
- `stable-diffusion-xl-1024-v1-0` (default)
- `stable-diffusion-v1-6`

### OpenAI
- `dall-e-3` (default, highest quality)
- `dall-e-2`

### Hugging Face
- `stabilityai/stable-diffusion-2-1` (default)
- `runwayml/stable-diffusion-v1-5`
- `CompVis/stable-diffusion-v1-4`

## Configuration Options

### Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | Required | Text description of the image |
| `negative_prompt` | str | None | Things to avoid in the image |
| `width` | int | 512 | Image width in pixels |
| `height` | int | 512 | Image height in pixels |
| `num_images` | int | 1 | Number of images to generate |
| `steps` | int | 30 | Number of inference steps |
| `guidance_scale` | float | 7.5 | How closely to follow the prompt |
| `seed` | int | None | Random seed for reproducibility |

### Output Settings

Generated images are saved to the `generated_images/` directory with:
- Image file (PNG format)
- Metadata JSON file with generation parameters

## Running Examples

The project includes comprehensive examples in `example_usage.py`:

```bash
python example_usage.py
```

To run specific examples, edit `example_usage.py` and uncomment the desired function calls.

## Troubleshooting

### "API key not found" Error
- Make sure you've created a `.env` file with your API keys
- Check that the key names match exactly: `STABILITY_API_KEY`, `OPENAI_API_KEY`, `HUGGINGFACE_TOKEN`

### "Model not found" Error
- Verify the model name is correct
- For Hugging Face models, ensure you have access to the model
- Some models may require authentication tokens

### Slow Generation
- Reduce the number of `steps` (try 20-30 instead of 50)
- Use smaller image sizes (512x512 instead of 1024x1024)
- Consider using a faster backend or model

### Out of Memory (Local Generation)
- Local generation requires significant GPU memory
- Try smaller image sizes
- Reduce batch size to 1
- Use API-based backends instead

## Best Practices

1. **Start Simple**: Begin with basic prompts and default settings
2. **Iterate**: Refine your prompts based on results
3. **Use Negative Prompts**: Specify what you don't want to improve results
4. **Experiment with Seeds**: Use seeds to reproduce good results
5. **Adjust Guidance Scale**: Higher values (8-12) follow prompts more closely
6. **Balance Quality vs Speed**: More steps = better quality but slower generation

## Project Structure

```
.
├── config.py              # Configuration and settings
├── image_generator.py     # Main agent class
├── example_usage.py       # Usage examples
├── requirements.txt       # Python dependencies
├── README_AGENT.md       # This file
├── .env                  # API keys (create this)
└── generated_images/     # Output directory (auto-created)
```

## API Costs

Be aware of API costs when using cloud-based backends:

- **Stability AI**: Pay per image generated
- **OpenAI DALL-E**: Pay per image, DALL-E 3 is more expensive than DALL-E 2
- **Hugging Face**: Free tier available with rate limits
- **Local**: Free but requires GPU hardware

## License

This project is for educational purposes as part of a data science learning repository.

## Contributing

Feel free to extend this agent with:
- Additional backends (Midjourney, Adobe Firefly, etc.)
- Image-to-image generation
- Inpainting and outpainting
- Style transfer
- Image upscaling

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example usage
3. Verify your API keys are correctly configured
4. Check the official documentation for your chosen backend

---

**Happy Image Generating! 🎨**
