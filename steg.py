from PIL import Image

def _to_bitstring(data: bytes) -> str:
    """Converts bytes data to a string of bits."""
    return ''.join(f'{byte:08b}' for byte in data)

def embed_data(input_image_path: str, output_image_path: str, data: bytes) -> None:
    """
    Embeds the given data into the input image and saves it as output image.
    The first 32 bits store the length of the data.
    """
    img = Image.open(input_image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    data_length = len(data)
    header = f'{data_length:032b}'
    data_bits = header + _to_bitstring(data)
    
    if len(data_bits) > len(pixels):
        raise ValueError("Data too large to hide in the provided image.")
    
    new_pixels = []
    bit_index = 0
    for pixel in pixels:
        r, g, b = pixel
        if bit_index < len(data_bits):
            # Modify the LSB of the red channel with one bit of data.
            bit = int(data_bits[bit_index])
            r = (r & ~1) | bit
            bit_index += 1
        new_pixels.append((r, g, b))
    
    img.putdata(new_pixels)
    img.save(output_image_path)

def extract_data(stego_image_path: str) -> bytes:
    """
    Extracts embedded data from a stego image.
    Reads the first 32 bits to get the data length and then retrieves the data.
    """
    img = Image.open(stego_image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    # Read header: first 32 bits represent the length of embedded data.
    header_bits = ''.join(str(pixels[i][0] & 1) for i in range(32))
    data_length = int(header_bits, 2)
    total_data_bits = data_length * 8
    
    data_bits = ''.join(str(pixels[i][0] & 1) for i in range(32, 32 + total_data_bits))
    
    data_bytes = [int(data_bits[i:i+8], 2) for i in range(0, len(data_bits), 8)]
    return bytes(data_bytes)
