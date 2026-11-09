import os
from PIL import Image

def compress_image(input_path, output_path, max_size_kb=128):
    """
    Compresses and saves an image as a JPG under a specified file size limit.
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert RGBA / PNG transparency to RGB for JPEG compatibility
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    # Start with high quality and lower it iteratively if needed
    quality = 95
    step = 5
    
    while quality > 10:
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        file_size_kb = os.path.getsize(output_path) / 1024
        
        if file_size_kb <= max_size_kb:
            print(f"Success! Compressed size: {file_size_kb:.2f} KB at quality={quality}")
            return
        
        quality -= step
        
    # Fallback: if it's still too large, reduce the dimensions slightly
    print("Reducing dimensions to meet file size target...")
    width, height = img.size
    img = img.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
    img.save(output_path, "JPEG", quality=75, optimize=True)
    
    final_size_kb = os.path.getsize(output_path) / 1024
    print(f"Resized & saved. Final size: {final_size_kb:.2f} KB")

# Run the function with your exact filename
compress_image("monrovia.liberia.jpg", "monrovia_compressed_128kb.jpg", max_size_kb=128)
