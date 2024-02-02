from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import pandas as pd
import os

def create_embeddings(model, device, text, images):
    combined_embeddings_list = []  # Store flattened embeddings here

    for image in images:

        inputs = {
            ModalityType.TEXT: data.load_and_transform_text(text, device),
            ModalityType.VISION: data.load_and_transform_vision_data([image], device)
        }

        with torch.no_grad():
            embeddings = model(inputs)

        vision_embedding = embeddings[ModalityType.VISION]
        text_embedding = embeddings[ModalityType.TEXT]

        combined_embedding = torch.cat((vision_embedding, text_embedding), dim=1)
        combined_embeddings_list.append(combined_embedding)

    return combined_embeddings_list

def flatten_embeddings(embeddings):
    flattened_embeddings = []
    for tensor in embeddings:
        flattened_tensor = tensor.cpu().numpy().flatten()
        flattened_embeddings.append(flattened_tensor.tolist())
    return flattened_embeddings

def write_embeddings(flattened_embeddings):
    embeddings_df = pd.DataFrame(flattened_embeddings) # create pandas dataframe
    csv_file_path = 'embeddings.csv'
    write_header = not os.path.exists(csv_file_path) # don't write header every time...
    embeddings_df.to_csv(csv_file_path, mode='a', index=False, header=write_header)
    print(f"Embeddings written to {csv_file_path}")

def initialize_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)
    return model,device

def get_data():
    # TODO use parsing scripts to get real data
    sample_title = ["MERCEDES BENZ FACTORY VINTAGE PARTS"]
    sample_images = [".assets/test_image_1.jpg",
                 ".assets/test_image_2.jpeg"]
    return sample_title, sample_images

def main():
    text,images = get_data()
    model,device = initialize_model()
    embeddings = create_embeddings(model, device, text, images)
    flattened_embeddings = flatten_embeddings(embeddings)
    write_embeddings(flattened_embeddings)

if __name__ == "__main__":
    main()
