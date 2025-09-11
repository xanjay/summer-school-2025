from utils import encode_image, create_ollama_client, detect_objects

client = create_ollama_client()

img = encode_image(r"vision_images/vision_config1.jpg")

print(detect_objects(client, img))
