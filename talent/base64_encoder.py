import base64
import os


os.chdir('./talent/static')
cwd = os.getcwd()

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_paths = {'flash_info':os.path.join(cwd,'flash_info.jpg'),'paris': os.path.join(cwd,'paris.png'),'region': os.path.join(cwd,'region.png'),'rf':os.path.join(cwd,'rf.png'),'rf_long':os.path.join(cwd,'rf_long.png'), 'square': os.path.join(cwd,'square.PNG'), 'texto':os.path.join(cwd,'texto.jpg')}
base64_images = {}

for key, value in image_paths.items():
    base64_images[key] = get_base64_encoded_image(value)

print(base64_images)



