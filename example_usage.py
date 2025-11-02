#!/usr/bin/env python3
"""
Example usage scripts for the Image Generation Agent
Demonstrates various features and use cases.
"""

from image_generation_agent import ImageGenerationAgent
from config import Config
import sys


def example_1_basic_generation():
    """Example 1: Basic image generation with default settings."""
    print("\n" + "="*60)
    print("Example 1: Basic Image Generation")
    print("="*60)
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        images = agent.generate(
            prompt="a serene mountain landscape at sunset",
            width=512,
            height=512,
            num_images=1
        )
        
        saved_paths = agent.save_images(
            images=images,
            output_dir="examples/basic",
            prefix="landscape"
        )
        
        print(f"✓ Generated {len(saved_paths)} image(s)")
        for path in saved_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_2_advanced_parameters():
    """Example 2: Using advanced parameters for better quality."""
    print("\n" + "="*60)
    print("Example 2: Advanced Parameters")
    print("="*60)
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        images = agent.generate(
            prompt="professional portrait photo of a person, studio lighting, 8k, highly detailed",
            negative_prompt="blurry, low quality, distorted, cartoon, anime",
            width=768,
            height=768,
            num_images=1,
            num_inference_steps=75,
            guidance_scale=8.0,
            seed=42  # For reproducibility
        )
        
        saved_paths = agent.save_images(
            images=images,
            output_dir="examples/advanced",
            prefix="portrait",
            prompt="professional portrait photo"
        )
        
        print(f"✓ Generated {len(saved_paths)} image(s) with seed 42")
        for path in saved_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_3_batch_generation():
    """Example 3: Generate multiple images at once."""
    print("\n" + "="*60)
    print("Example 3: Batch Generation")
    print("="*60)
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        images = agent.generate(
            prompt="cute robot character design, colorful, friendly",
            negative_prompt="scary, dark, realistic",
            width=512,
            height=512,
            num_images=4,
            num_inference_steps=50,
            guidance_scale=7.5
        )
        
        saved_paths = agent.save_images(
            images=images,
            output_dir="examples/batch",
            prefix="robot"
        )
        
        print(f"✓ Generated {len(saved_paths)} images in batch")
        for i, path in enumerate(saved_paths, 1):
            print(f"  {i}. {path}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_4_different_styles():
    """Example 4: Generate images in different artistic styles."""
    print("\n" + "="*60)
    print("Example 4: Different Artistic Styles")
    print("="*60)
    
    styles = [
        ("oil painting of a forest, impressionist style", "oil_painting"),
        ("digital art of a cyberpunk city, neon lights", "digital_art"),
        ("watercolor painting of flowers, soft colors", "watercolor"),
        ("pencil sketch of a cat, detailed line art", "sketch")
    ]
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        for prompt, style_name in styles:
            print(f"\nGenerating: {style_name}")
            
            images = agent.generate(
                prompt=prompt,
                width=512,
                height=512,
                num_images=1,
                num_inference_steps=50
            )
            
            saved_paths = agent.save_images(
                images=images,
                output_dir="examples/styles",
                prefix=style_name
            )
            
            print(f"  ✓ Saved: {saved_paths[0]}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_5_with_config():
    """Example 5: Using configuration file."""
    print("\n" + "="*60)
    print("Example 5: Using Configuration File")
    print("="*60)
    
    try:
        # Load configuration
        config = Config()
        
        # Get settings from config
        backend = config.get('backend')
        width = config.get('generation.width')
        height = config.get('generation.height')
        steps = config.get('generation.num_inference_steps')
        guidance = config.get('generation.guidance_scale')
        
        print(f"Using configuration:")
        print(f"  Backend: {backend}")
        print(f"  Size: {width}x{height}")
        print(f"  Steps: {steps}")
        print(f"  Guidance: {guidance}")
        
        agent = ImageGenerationAgent(backend=backend)
        
        images = agent.generate(
            prompt="a magical fantasy castle on a floating island",
            width=width,
            height=height,
            num_images=1,
            num_inference_steps=steps,
            guidance_scale=guidance
        )
        
        output_dir = config.get('output.directory')
        prefix = config.get('output.prefix')
        
        saved_paths = agent.save_images(
            images=images,
            output_dir=output_dir,
            prefix=prefix
        )
        
        print(f"\n✓ Generated using config settings")
        for path in saved_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_6_reproducible_results():
    """Example 6: Generate reproducible results using seeds."""
    print("\n" + "="*60)
    print("Example 6: Reproducible Results with Seeds")
    print("="*60)
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        prompt = "a cozy coffee shop interior, warm lighting"
        seed = 12345
        
        print(f"Generating with seed {seed} (run 1)...")
        images1 = agent.generate(
            prompt=prompt,
            width=512,
            height=512,
            num_images=1,
            seed=seed
        )
        
        print(f"Generating with seed {seed} (run 2)...")
        images2 = agent.generate(
            prompt=prompt,
            width=512,
            height=512,
            num_images=1,
            seed=seed
        )
        
        saved_paths1 = agent.save_images(images1, "examples/reproducible", "run1")
        saved_paths2 = agent.save_images(images2, "examples/reproducible", "run2")
        
        print(f"\n✓ Generated identical images using seed {seed}")
        print(f"  Run 1: {saved_paths1[0]}")
        print(f"  Run 2: {saved_paths2[0]}")
        print(f"  (These should be identical)")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def example_7_openai_dalle():
    """Example 7: Using OpenAI DALL-E (requires API key)."""
    print("\n" + "="*60)
    print("Example 7: OpenAI DALL-E Generation")
    print("="*60)
    
    import os
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠ Skipping: OPENAI_API_KEY not set")
        print("  Set it with: export OPENAI_API_KEY='your-key'")
        return
    
    try:
        agent = ImageGenerationAgent(backend='openai', model='dall-e-3')
        
        images = agent.generate(
            prompt="a futuristic city with flying cars and neon lights",
            width=1024,
            height=1024,
            num_images=1
        )
        
        saved_paths = agent.save_images(
            images=images,
            output_dir="examples/openai",
            prefix="dalle"
        )
        
        print(f"✓ Generated with DALL-E 3")
        for path in saved_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def example_8_comparison():
    """Example 8: Compare different guidance scales."""
    print("\n" + "="*60)
    print("Example 8: Guidance Scale Comparison")
    print("="*60)
    
    try:
        agent = ImageGenerationAgent(backend='huggingface')
        
        prompt = "a red apple on a wooden table"
        guidance_scales = [5.0, 7.5, 10.0, 15.0]
        
        for guidance in guidance_scales:
            print(f"\nGenerating with guidance scale {guidance}...")
            
            images = agent.generate(
                prompt=prompt,
                width=512,
                height=512,
                num_images=1,
                num_inference_steps=50,
                guidance_scale=guidance,
                seed=999  # Same seed for fair comparison
            )
            
            saved_paths = agent.save_images(
                images=images,
                output_dir="examples/comparison",
                prefix=f"guidance_{guidance}"
            )
            
            print(f"  ✓ Saved: {saved_paths[0]}")
        
        print(f"\n✓ Generated {len(guidance_scales)} images with different guidance scales")
        print("  Compare them to see the effect of guidance scale!")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all examples or specific ones."""
    examples = {
        '1': ('Basic Generation', example_1_basic_generation),
        '2': ('Advanced Parameters', example_2_advanced_parameters),
        '3': ('Batch Generation', example_3_batch_generation),
        '4': ('Different Styles', example_4_different_styles),
        '5': ('With Config', example_5_with_config),
        '6': ('Reproducible Results', example_6_reproducible_results),
        '7': ('OpenAI DALL-E', example_7_openai_dalle),
        '8': ('Guidance Comparison', example_8_comparison),
    }
    
    print("\n" + "="*60)
    print("Image Generation Agent - Example Usage")
    print("="*60)
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  all. Run all examples")
    print("  q. Quit")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nSelect example (1-8, all, or q): ").strip().lower()
    
    if choice == 'q':
        print("Goodbye!")
        return
    
    if choice == 'all':
        for name, func in examples.values():
            try:
                func()
            except KeyboardInterrupt:
                print("\n\n⚠ Interrupted by user")
                break
            except Exception as e:
                print(f"\n✗ Example failed: {e}")
                continue
    elif choice in examples:
        name, func = examples[choice]
        func()
    else:
        print(f"Invalid choice: {choice}")
        return
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
    print("\nCheck the 'examples/' directory for generated images.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
