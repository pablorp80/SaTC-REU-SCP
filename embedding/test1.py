from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms

# Rewritten version of imagebind.data.load_and_transform_vision_data
# that takes urls instead of file paths, because downloading all
# images locally is unreasonable
def load_and_transform_vision_data_from_web(image_urls, device):
    if image_urls is None:
        return None

    image_outputs = []

    # Same transformations as in original function
    data_transform = transforms.Compose([
        transforms.Resize(224, interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.48145466, 0.4578275, 0.40821073),
                             std=(0.26862954, 0.26130258, 0.27577711)),
    ])

    for image_url in image_urls:
        try:
            response = requests.get(image_url)
        except:
            print('Request error for URL!')
            return None
        image = Image.open(BytesIO(response.content)).convert("RGB")

        image = data_transform(image).to(device)
        image_outputs.append(image)

    return torch.stack(image_outputs, dim=0)

sample_title = ["MERCEDES BENZ FACTORY VINTAGE PARTS"]
sample_images = ["https://images.craigslist.org/00V0V_9uMUlJQALlX_07K037_600x450.jpg"]

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = imagebind_model.imagebind_huge(pretrained=True)
model.eval()
model.to(device)

inputs = {
        ModalityType.TEXT: data.load_and_transform_text(sample_title, device),
        ModalityType.VISION: load_and_transform_vision_data_from_web(sample_images, device)
}

with torch.no_grad():
    embeddings = model(inputs)

vision_embedding = embeddings[ModalityType.VISION]
text_embedding = embeddings[ModalityType.TEXT]

# If you want a combined embedding, you can concatenate or otherwise combine these
combined_embedding = torch.cat((vision_embedding, text_embedding), dim=1)

print("Combined Embedding:", combined_embedding)
