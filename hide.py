from PIL import Image


def message_to_bits(message):
    """
    Convertit un message texte en une chaîne de bits.
    """
    return ''.join([format(ord(c), '08b') for c in message]) + '1111111111111110'  # Marqueur de fin

def bits_to_message(bits):
    """
    Convertit une chaîne de bits en message texte.
    """
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''
    for c in chars:
        if c == '11111111': continue
        if c == '11111110': break  # Marqueur de fin
        message += chr(int(c, 2))
    return message

def encode(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = message_to_bits(message)
    pixels = list(img.getdata())

    new_pixels = []
    bit_index = 0
    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # R, G, B
            if bit_index < len(binary_message):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[bit_index])
                bit_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_path)
    print("Message caché dans", output_path)

def decode(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    bits = ''
    for pixel in pixels:
        for i in range(3):  # R, G, B
            bits += str(pixel[i] & 1)
    message = bits_to_message(bits)
    print("Message extrait :", message)



if __name__ == "__main__":
    encode("image.png", "Ceci est un secret !", "image_stego.png")
    decode("image_stego.png")