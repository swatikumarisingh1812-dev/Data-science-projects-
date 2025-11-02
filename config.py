"""
Configuration file for AI Image Generator Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for image generation settings"""
    
    # API Keys (load from environment variables)
    STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
    
    # Default generation settings
    DEFAULT_WIDTH = 512
    DEFAULT_HEIGHT = 512
    DEFAULT_STEPS = 30
    DEFAULT_GUIDANCE_SCALE = 7.5
    DEFAULT_NUM_IMAGES = 1
    
    # Output settings
    OUTPUT_DIR = 'generated_images'
    DEFAULT_FORMAT = 'PNG'
    
    # API Endpoints
    STABILITY_API_URL = 'https://api.stability.ai/v1/generation'
    
    # Model options
    AVAILABLE_MODELS = {
        'stability': [
            'stable-diffusion-xl-1024-v1-0',
            'stable-diffusion-v1-6',
        ],
        'huggingface': [
            'stabilityai/stable-diffusion-2-1',
            'runwayml/stable-diffusion-v1-5',
            'CompVis/stable-diffusion-v1-4',
        ],
        'openai': [
            'dall-e-3',
            'dall-e-2',
        ]
    }
    
    # Default models for each backend
    DEFAULT_STABILITY_MODEL = 'stable-diffusion-xl-1024-v1-0'
    DEFAULT_HUGGINGFACE_MODEL = 'stabilityai/stable-diffusion-2-1'
    DEFAULT_OPENAI_MODEL = 'dall-e-3'
    
    @classmethod
    def validate_api_keys(cls):
        """Check which API keys are configured"""
        available_backends = []
        
        if cls.STABILITY_API_KEY:
            available_backends.append('stability')
        if cls.OPENAI_API_KEY:
            available_backends.append('openai')
        if cls.HUGGINGFACE_TOKEN:
            available_backends.append('huggingface')
            
        return available_backends
    
    @classmethod
    def get_output_dir(cls):
        """Get or create output directory"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return cls.OUTPUT_DIR
