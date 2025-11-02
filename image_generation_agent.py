#!/usr/bin/env python3
"""
AI Image Generation Agent
A versatile image generation tool supporting multiple AI backends.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from PIL import Image as PILImage
else:
    try:
        from PIL import Image as PILImage
    except ImportError:
        PILImage = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImageGenerationAgent:
    """Main agent class for AI image generation."""
    
    SUPPORTED_BACKENDS = ['huggingface', 'openai', 'stability']
    
    def __init__(self, backend: str = 'huggingface', model: Optional[str] = None):
        """
        Initialize the image generation agent.
        
        Args:
            backend: AI backend to use ('huggingface', 'openai', 'stability')
            model: Specific model name (optional, uses defaults if not provided)
        """
        self.backend = backend.lower()
        self.model = model
        self.generator = None
        
        if self.backend not in self.SUPPORTED_BACKENDS:
            raise ValueError(f"Backend must be one of {self.SUPPORTED_BACKENDS}")
        
        self._initialize_backend()
    
    def _initialize_backend(self):
        """Initialize the selected backend."""
        logger.info(f"Initializing {self.backend} backend...")
        
        if self.backend == 'huggingface':
            self._init_huggingface()
        elif self.backend == 'openai':
            self._init_openai()
        elif self.backend == 'stability':
            self._init_stability()
    
    def _init_huggingface(self):
        """Initialize Hugging Face Diffusers backend."""
        try:
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
            import torch
            
            model_id = self.model or "stabilityai/stable-diffusion-2-1"
            
            logger.info(f"Loading model: {model_id}")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Load the pipeline
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Use DPM-Solver for faster generation
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
            pipe = pipe.to(device)
            
            # Enable memory optimizations
            if device == "cuda":
                pipe.enable_attention_slicing()
            
            self.generator = pipe
            logger.info("Hugging Face backend initialized successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import required libraries: {e}")
            logger.error("Install with: pip install diffusers transformers torch accelerate")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to initialize Hugging Face backend: {e}")
            sys.exit(1)
    
    def _init_openai(self):
        """Initialize OpenAI DALL-E backend."""
        try:
            import openai
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            openai.api_key = api_key
            self.generator = openai
            self.model = self.model or "dall-e-3"
            
            logger.info("OpenAI backend initialized successfully")
            
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI backend: {e}")
            sys.exit(1)
    
    def _init_stability(self):
        """Initialize Stability AI backend."""
        try:
            import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
            from stability_sdk import client
            
            api_key = os.getenv('STABILITY_API_KEY')
            if not api_key:
                raise ValueError("STABILITY_API_KEY environment variable not set")
            
            self.generator = client.StabilityInference(
                key=api_key,
                verbose=True,
            )
            
            logger.info("Stability AI backend initialized successfully")
            
        except ImportError:
            logger.error("Stability SDK not installed. Install with: pip install stability-sdk")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to initialize Stability AI backend: {e}")
            sys.exit(1)
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> List:
        """
        Generate images from text prompt.
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the image
            width: Image width in pixels
            height: Image height in pixels
            num_images: Number of images to generate
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducibility
            
        Returns:
            List of PIL Image objects
        """
        logger.info(f"Generating {num_images} image(s) with prompt: '{prompt}'")
        
        if self.backend == 'huggingface':
            return self._generate_huggingface(
                prompt, negative_prompt, width, height,
                num_images, num_inference_steps, guidance_scale, seed
            )
        elif self.backend == 'openai':
            return self._generate_openai(prompt, width, height, num_images)
        elif self.backend == 'stability':
            return self._generate_stability(
                prompt, width, height, num_images, num_inference_steps, guidance_scale, seed
            )
    
    def _generate_huggingface(
        self, prompt, negative_prompt, width, height,
        num_images, num_inference_steps, guidance_scale, seed
    ):
        """Generate images using Hugging Face Diffusers."""
        import torch
        
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.generator.device).manual_seed(seed)
        
        result = self.generator(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_images_per_prompt=num_images,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        return result.images
    
    def _generate_openai(self, prompt, width, height, num_images):
        """Generate images using OpenAI DALL-E."""
        import requests
        from io import BytesIO
        from PIL import Image
        
        # DALL-E 3 only supports specific sizes
        size_map = {
            (1024, 1024): "1024x1024",
            (1792, 1024): "1792x1024",
            (1024, 1792): "1024x1792"
        }
        
        size = size_map.get((width, height), "1024x1024")
        logger.info(f"Using size: {size} (DALL-E 3 constraint)")
        
        images = []
        for i in range(num_images):
            response = self.generator.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            
            # Download the image
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            images.append(image)
            
            logger.info(f"Generated image {i+1}/{num_images}")
        
        return images
    
    def _generate_stability(self, prompt, width, height, num_images, num_inference_steps, guidance_scale, seed):
        """Generate images using Stability AI."""
        import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
        from PIL import Image
        from io import BytesIO
        
        images = []
        
        answers = self.generator.generate(
            prompt=prompt,
            width=width,
            height=height,
            samples=num_images,
            steps=num_inference_steps,
            cfg_scale=guidance_scale,
            seed=seed or 0
        )
        
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    logger.warning("Image filtered by safety checker")
                    continue
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(BytesIO(artifact.binary))
                    images.append(img)
        
        return images
    
    def save_images(
        self,
        images: List,
        output_dir: str = "generated_images",
        prefix: str = "image",
        prompt: Optional[str] = None
    ) -> List[str]:
        """
        Save generated images to disk.
        
        Args:
            images: List of PIL Image objects
            output_dir: Directory to save images
            prefix: Filename prefix
            prompt: Original prompt (saved in metadata if provided)
            
        Returns:
            List of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_paths = []
        
        for i, image in enumerate(images):
            filename = f"{prefix}_{timestamp}_{i+1}.png"
            filepath = output_path / filename
            
            # Save with metadata
            if prompt and hasattr(image, 'info'):
                from PIL import PngImagePlugin
                metadata = PngImagePlugin.PngInfo()
                metadata.add_text("prompt", prompt)
                metadata.add_text("backend", self.backend)
                metadata.add_text("timestamp", timestamp)
                image.save(filepath, pnginfo=metadata)
            else:
                image.save(filepath)
            
            saved_paths.append(str(filepath))
            logger.info(f"Saved: {filepath}")
        
        return saved_paths


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Image Generation Agent - Generate images from text prompts"
    )
    
    parser.add_argument(
        'prompt',
        type=str,
        help='Text description of the image to generate'
    )
    
    parser.add_argument(
        '--backend',
        type=str,
        default='huggingface',
        choices=['huggingface', 'openai', 'stability'],
        help='AI backend to use (default: huggingface)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        help='Specific model to use (optional)'
    )
    
    parser.add_argument(
        '--negative-prompt',
        type=str,
        help='Things to avoid in the image'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=512,
        help='Image width in pixels (default: 512)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=512,
        help='Image height in pixels (default: 512)'
    )
    
    parser.add_argument(
        '--num-images',
        type=int,
        default=1,
        help='Number of images to generate (default: 1)'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=50,
        help='Number of inference steps (default: 50)'
    )
    
    parser.add_argument(
        '--guidance-scale',
        type=float,
        default=7.5,
        help='Guidance scale - how closely to follow prompt (default: 7.5)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='generated_images',
        help='Output directory for images (default: generated_images)'
    )
    
    parser.add_argument(
        '--prefix',
        type=str,
        default='image',
        help='Filename prefix (default: image)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = ImageGenerationAgent(backend=args.backend, model=args.model)
        
        # Generate images
        images = agent.generate(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            width=args.width,
            height=args.height,
            num_images=args.num_images,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance_scale,
            seed=args.seed
        )
        
        # Save images
        saved_paths = agent.save_images(
            images=images,
            output_dir=args.output_dir,
            prefix=args.prefix,
            prompt=args.prompt
        )
        
        logger.info(f"Successfully generated {len(saved_paths)} image(s)")
        print("\n✓ Generation complete!")
        print(f"Images saved to: {args.output_dir}")
        for path in saved_paths:
            print(f"  - {path}")
        
    except KeyboardInterrupt:
        logger.info("Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
