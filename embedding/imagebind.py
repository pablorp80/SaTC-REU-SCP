from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType

sample_title = ["MERCEDES BENZ FACTORY VINTAGE PARTS"]
sample_images = [".assets/test_image_1.jpg",
                 ".assets/test_image_2.jpeg"]

device = "cuda:0" if torch.cuda.is_available() else "cpu"

model = imagebind_model.imagebind_huge(pretrained=True)
model.eval()
model.to(device)

combined_embeddings = []

for image in sample_images:

    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(sample_title, device),
        ModalityType.VISION: data.load_and_transform_vision_data([image], device)
    }

    with torch.no_grad():
        embeddings = model(inputs)

    vision_embedding = embeddings[ModalityType.VISION]
    text_embedding = embeddings[ModalityType.TEXT]

    combined_embedding = torch.cat((vision_embedding, text_embedding), dim=1)
    combined_embeddings.append(combined_embedding)

for embedding in combined_embeddings:
    print(embedding)
    print ('\n------\n')
