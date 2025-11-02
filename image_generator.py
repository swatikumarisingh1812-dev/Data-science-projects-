"""
AI Image Generator Agent
Supports multiple backends for image generation
"""
import os
import json
import time
import base64
from datetime import datetime
from typing import Optional, List, Dict, Any
from io import BytesIO

import requests
from PIL import Image
from config import Config


class ImageGeneratorAgent:
    """AI Agent for generating images from text prompts"""
    
    def __init__(self, backend: str = 'stability', model: Optional[str] = None):
        """
        Initialize the image generator agent
        
        Args:
            backend: Backend to use ('stability', 'openai', 'huggingface', 'local')
            model: Specific model to use (optional, uses default if not specified)
        """
        self.backend = backend.lower()
        self.model = model
        self.config = Config()
        
        # Set default model if not specified
        if not self.model:
            if self.backend == 'stability':
                self.model = self.config.DEFAULT_STABILITY_MODEL
            elif self.backend == 'huggingface':
                self.model = self.config.DEFAULT_HUGGINGFACE_MODEL
            elif self.backend == 'openai':
                self.model = self.config.DEFAULT_OPENAI_MODEL
        
        # Validate backend
        self._validate_backend()
    
    def _validate_backend(self):
        """Validate that the selected backend is properly configured"""
        available = self.config.validate_api_keys()
        
        if self.backend == 'stability' and 'stability' not in available:
            raise ValueError(
                "Stability AI backend selected but STABILITY_API_KEY not found. "
                "Please set it in your .env file."
            )
        elif self.backend == 'openai' and 'openai' not in available:
            raise ValueError(
                "OpenAI backend selected but OPENAI_API_KEY not found. "
                "Please set it in your .env file."
            )
        elif self.backend == 'huggingface' and self.backend != 'local':
            if 'huggingface' not in available:
                print("Warning: HUGGINGFACE_TOKEN not found. Some models may not be accessible.")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = None,
        height: int = None,
        num_images: int = 1,
        steps: int = None,
        guidance_scale: float = None,
        seed: Optional[int] = None,
        **kwargs
    ) -> List[Image.Image]:
        """
        Generate images from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            negative_prompt: Things to avoid in the generation
            width: Image width (default from config)
            height: Image height (default from config)
            num_images: Number of images to generate
            steps: Number of inference steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducibility
            **kwargs: Additional backend-specific parameters
            
        Returns:
            List of PIL Image objects
        """
        # Set defaults
        width = width or self.config.DEFAULT_WIDTH
        height = height or self.config.DEFAULT_HEIGHT
        steps = steps or self.config.DEFAULT_STEPS
        guidance_scale = guidance_scale or self.config.DEFAULT_GUIDANCE_SCALE
        
        print(f"Generating {num_images} image(s) with {self.backend} backend...")
        print(f"Prompt: {prompt}")
        
        # Route to appropriate backend
        if self.backend == 'stability':
            return self._generate_stability(
                prompt, negative_prompt, width, height, 
                num_images, steps, guidance_scale, seed, **kwargs
            )
        elif self.backend == 'openai':
            return self._generate_openai(
                prompt, width, height, num_images, **kwargs
            )
        elif self.backend == 'huggingface':
            return self._generate_huggingface(
                prompt, negative_prompt, width, height,
                num_images, steps, guidance_scale, seed, **kwargs
            )
        elif self.backend == 'local':
            return self._generate_local(
                prompt, negative_prompt, width, height,
                num_images, steps, guidance_scale, seed, **kwargs
            )
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _generate_stability(
        self, prompt, negative_prompt, width, height,
        num_images, steps, guidance_scale, seed, **kwargs
    ) -> List[Image.Image]:
        """Generate images using Stability AI API"""
        url = f"{self.config.STABILITY_API_URL}/{self.model}/text-to-image"
        
        headers = {
            "Authorization": f"Bearer {self.config.STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        body = {
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": guidance_scale,
            "height": height,
            "width": width,
            "steps": steps,
            "samples": num_images,
        }
        
        if negative_prompt:
            body["text_prompts"].append({"text": negative_prompt, "weight": -1})
        
        if seed is not None:
            body["seed"] = seed
        
        response = requests.post(url, headers=headers, json=body)
        
        if response.status_code != 200:
            raise Exception(f"Stability AI API error: {response.text}")
        
        data = response.json()
        images = []
        
        for artifact in data.get("artifacts", []):
            if artifact.get("finishReason") == "SUCCESS":
                image_data = base64.b64decode(artifact["base64"])
                image = Image.open(BytesIO(image_data))
                images.append(image)
        
        return images
    
    def _generate_openai(
        self, prompt, width, height, num_images, **kwargs
    ) -> List[Image.Image]:
        """Generate images using OpenAI DALL-E API"""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. "
                "Install it with: pip install openai"
            )
        
        client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
        
        # DALL-E 3 only supports 1 image at a time
        if self.model == 'dall-e-3':
            num_images = 1
            size = f"{width}x{height}" if width == height else "1024x1024"
        else:
            size = f"{width}x{height}"
        
        images = []
        
        for _ in range(num_images):
            response = client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=kwargs.get('quality', 'standard'),
                n=1
            )
            
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            images.append(image)
        
        return images
    
    def _generate_huggingface(
        self, prompt, negative_prompt, width, height,
        num_images, steps, guidance_scale, seed, **kwargs
    ) -> List[Image.Image]:
        """Generate images using Hugging Face Inference API"""
        api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        headers = {}
        if self.config.HUGGINGFACE_TOKEN:
            headers["Authorization"] = f"Bearer {self.config.HUGGINGFACE_TOKEN}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": steps,
                "guidance_scale": guidance_scale,
            }
        }
        
        if negative_prompt:
            payload["parameters"]["negative_prompt"] = negative_prompt
        
        if seed is not None:
            payload["parameters"]["seed"] = seed
        
        images = []
        
        for _ in range(num_images):
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"Hugging Face API error: {response.text}")
            
            image = Image.open(BytesIO(response.content))
            images.append(image)
            
            time.sleep(1)
        
        return images
    
    def _generate_local(
        self, prompt, negative_prompt, width, height,
        num_images, steps, guidance_scale, seed, **kwargs
    ) -> List[Image.Image]:
        """Generate images using local diffusers pipeline"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
        except ImportError:
            raise ImportError(
                "Diffusers and torch not installed. "
                "Install them with: pip install torch diffusers transformers accelerate"
            )
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_auth_token=self.config.HUGGINGFACE_TOKEN or None
        )
        pipe = pipe.to(device)
        
        generator = torch.Generator(device=device)
        if seed is not None:
            generator = generator.manual_seed(seed)
        
        result = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_images_per_prompt=num_images,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        return result.images
    
    def save_images(
        self,
        images: List[Image.Image],
        prompt: str,
        prefix: str = "generated",
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Save generated images to disk
        
        Args:
            images: List of PIL Images to save
            prompt: The prompt used to generate the images
            prefix: Filename prefix
            metadata: Additional metadata to save
            
        Returns:
            List of saved file paths
        """
        output_dir = self.config.get_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_paths = []
        
        for idx, image in enumerate(images):
            filename = f"{prefix}_{timestamp}_{idx+1}.{self.config.DEFAULT_FORMAT.lower()}"
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            image.save(filepath, format=self.config.DEFAULT_FORMAT)
            saved_paths.append(filepath)
            
            # Save metadata
            meta = {
                "prompt": prompt,
                "backend": self.backend,
                "model": self.model,
                "timestamp": timestamp,
                "size": image.size,
            }
            if metadata:
                meta.update(metadata)
            
            meta_filepath = filepath.replace(
                f".{self.config.DEFAULT_FORMAT.lower()}", 
                ".json"
            )
            with open(meta_filepath, 'w') as f:
                json.dump(meta, f, indent=2)
            
            print(f"Saved: {filepath}")
        
        return saved_paths
    
    def batch_generate(
        self,
        prompts: List[str],
        **kwargs
    ) -> Dict[str, List[Image.Image]]:
        """
        Generate images for multiple prompts
        
        Args:
            prompts: List of text prompts
            **kwargs: Generation parameters
            
        Returns:
            Dictionary mapping prompts to generated images
        """
        results = {}
        
        for prompt in prompts:
            print(f"\n{'='*60}")
            try:
                images = self.generate(prompt, **kwargs)
                results[prompt] = images
            except Exception as e:
                print(f"Error generating images for prompt '{prompt}': {e}")
                results[prompt] = []
        
        return results
    
    @staticmethod
    def list_available_backends() -> Dict[str, bool]:
        """Check which backends are available"""
        available = Config.validate_api_keys()
        
        return {
            'stability': 'stability' in available,
            'openai': 'openai' in available,
            'huggingface': True,
            'local': True
        }
    
    @staticmethod
    def get_available_models(backend: str) -> List[str]:
        """Get list of available models for a backend"""
        return Config.AVAILABLE_MODELS.get(backend, [])


if __name__ == "__main__":
    print("AI Image Generator Agent")
    print("=" * 60)
    print("\nAvailable backends:")
    backends = ImageGeneratorAgent.list_available_backends()
    for backend, available in backends.items():
        status = "✓" if available else "✗"
        print(f"  {status} {backend}")
    
    print("\nTo use this agent, import it in your Python script:")
    print("  from image_generator import ImageGeneratorAgent")
    print("\nSee example_usage.py for detailed examples.")
