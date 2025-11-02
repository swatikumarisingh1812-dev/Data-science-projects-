"""
Example usage of the AI Image Generator Agent
"""
from image_generator import ImageGeneratorAgent


def example_basic_generation():
    """Basic image generation example"""
    print("\n" + "="*60)
    print("Example 1: Basic Image Generation")
    print("="*60)
    
    # Initialize agent with Stability AI backend
    agent = ImageGeneratorAgent(backend='stability')
    
    # Generate a single image
    prompt = "A serene mountain landscape at sunset, digital art"
    images = agent.generate(
        prompt=prompt,
        width=512,
        height=512,
        num_images=1
    )
    
    # Save the generated images
    agent.save_images(images, prompt=prompt, prefix="mountain")
    
    print(f"Generated {len(images)} image(s)")


def example_with_negative_prompt():
    """Example using negative prompts"""
    print("\n" + "="*60)
    print("Example 2: Using Negative Prompts")
    print("="*60)
    
    agent = ImageGeneratorAgent(backend='stability')
    
    prompt = "A cute robot playing with a cat, cartoon style"
    negative_prompt = "scary, dark, horror, realistic"
    
    images = agent.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=512,
        height=512,
        num_images=2,
        guidance_scale=8.0
    )
    
    agent.save_images(
        images, 
        prompt=prompt,
        prefix="robot_cat",
        metadata={"negative_prompt": negative_prompt}
    )


def example_batch_generation():
    """Example of batch generation with multiple prompts"""
    print("\n" + "="*60)
    print("Example 3: Batch Generation")
    print("="*60)
    
    agent = ImageGeneratorAgent(backend='stability')
    
    prompts = [
        "A futuristic city with flying cars, cyberpunk style",
        "A peaceful zen garden with cherry blossoms",
        "An underwater scene with colorful coral reefs"
    ]
    
    results = agent.batch_generate(
        prompts=prompts,
        width=512,
        height=512,
        num_images=1
    )
    
    # Save all generated images
    for prompt, images in results.items():
        if images:
            agent.save_images(images, prompt=prompt, prefix="batch")


def example_huggingface_backend():
    """Example using Hugging Face backend"""
    print("\n" + "="*60)
    print("Example 4: Hugging Face Backend")
    print("="*60)
    
    agent = ImageGeneratorAgent(
        backend='huggingface',
        model='stabilityai/stable-diffusion-2-1'
    )
    
    prompt = "A magical forest with glowing mushrooms, fantasy art"
    
    images = agent.generate(
        prompt=prompt,
        width=512,
        height=512,
        num_images=1,
        steps=25
    )
    
    agent.save_images(images, prompt=prompt, prefix="forest")


def example_with_seed():
    """Example using seed for reproducible results"""
    print("\n" + "="*60)
    print("Example 5: Reproducible Generation with Seed")
    print("="*60)
    
    agent = ImageGeneratorAgent(backend='stability')
    
    prompt = "A steampunk airship flying through clouds"
    seed = 42
    
    # Generate the same image twice with the same seed
    images1 = agent.generate(prompt=prompt, seed=seed, num_images=1)
    images2 = agent.generate(prompt=prompt, seed=seed, num_images=1)
    
    agent.save_images(images1, prompt=prompt, prefix="airship_1")
    agent.save_images(images2, prompt=prompt, prefix="airship_2")
    
    print("Both images should be identical (same seed)")


def example_openai_dalle():
    """Example using OpenAI DALL-E"""
    print("\n" + "="*60)
    print("Example 6: OpenAI DALL-E")
    print("="*60)
    
    try:
        agent = ImageGeneratorAgent(
            backend='openai',
            model='dall-e-3'
        )
        
        prompt = "A photorealistic image of a golden retriever wearing sunglasses"
        
        images = agent.generate(
            prompt=prompt,
            num_images=1,
            quality='standard'
        )
        
        agent.save_images(images, prompt=prompt, prefix="dalle")
        
    except ValueError as e:
        print(f"OpenAI backend not configured: {e}")


def example_local_generation():
    """Example using local model (requires GPU and more resources)"""
    print("\n" + "="*60)
    print("Example 7: Local Generation")
    print("="*60)
    
    try:
        agent = ImageGeneratorAgent(
            backend='local',
            model='runwayml/stable-diffusion-v1-5'
        )
        
        prompt = "A beautiful sunset over the ocean, oil painting"
        
        images = agent.generate(
            prompt=prompt,
            width=512,
            height=512,
            num_images=1,
            steps=30
        )
        
        agent.save_images(images, prompt=prompt, prefix="local")
        
    except ImportError as e:
        print(f"Local generation requires additional packages: {e}")
    except Exception as e:
        print(f"Error with local generation: {e}")


def check_available_backends():
    """Check which backends are available"""
    print("\n" + "="*60)
    print("Checking Available Backends")
    print("="*60)
    
    backends = ImageGeneratorAgent.list_available_backends()
    
    print("\nBackend Status:")
    for backend, available in backends.items():
        status = "✓ Available" if available else "✗ Not configured"
        print(f"  {backend:15} {status}")
        
        if available or backend in ['huggingface', 'local']:
            models = ImageGeneratorAgent.get_available_models(backend)
            print(f"    Models: {', '.join(models[:3])}")
    
    print("\nNote: To use API backends, set the appropriate API keys in .env file:")
    print("  - STABILITY_API_KEY for Stability AI")
    print("  - OPENAI_API_KEY for OpenAI DALL-E")
    print("  - HUGGINGFACE_TOKEN for Hugging Face (optional)")


if __name__ == "__main__":
    print("AI Image Generator Agent - Examples")
    print("="*60)
    
    # First, check available backends
    check_available_backends()
    
    print("\n\nTo run examples, uncomment the desired function calls below:")
    print("Note: Make sure you have configured the appropriate API keys in .env file")
    
    # Uncomment the examples you want to run:
    
    # example_basic_generation()
    # example_with_negative_prompt()
    # example_batch_generation()
    # example_huggingface_backend()
    # example_with_seed()
    # example_openai_dalle()
    # example_local_generation()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("Check the 'generated_images' folder for output")
