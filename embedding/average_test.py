from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import pandas as pd
import os
import random
from parsing.parse_craigslist import get_image_file_names

def create_embedding(model, device, text, images):
    combined_embeddings_list = []  # Store flattened embeddings here

    for image in images:

        image = '.assets/images/' + image

        inputs = {
            ModalityType.TEXT: data.load_and_transform_text(text, device),
            ModalityType.VISION: data.load_and_transform_vision_data([image], device)
        }

        with torch.no_grad():
            embeddings = model(inputs)

        vision_embedding = embeddings[ModalityType.VISION]
        text_embedding = embeddings[ModalityType.TEXT]

        embedding_average = (text_embedding + vision_embedding) / 2

        combined_embeddings_list.append(embedding_average)

    return combined_embeddings_list

def flatten_embedding(embedding):
    flattened_tensor = embedding.cpu().numpy().flatten()
    return flattened_tensor

def write_embeddings(flattened_embeddings):
    try:
        embeddings_df = pd.DataFrame(flattened_embeddings) # create pandas dataframe
        csv_file_path = 'embeddings.csv'
        write_header = not os.path.exists(csv_file_path) # don't write header every time...
        embeddings_df.to_csv(csv_file_path, mode='a', index=False, header=write_header)
        print(f"Embeddings written to {csv_file_path}")
        return True
    except:
        print("Error writing embeddings")
        return False

def initialize_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = imagebind_model.imagebind_huge(pretrained=True)
    model.eval()
    model.to(device)
    return model,device

def get_data():

    id_text_imagepaths = get_image_file_names()
    valid_posts = []
    for post in id_text_imagepaths:
        _, _, image_paths = post
        if image_paths:
            if all(os.path.exists('.assets/images/' + image) for image in image_paths):
                valid_posts.append(post)

    return valid_posts

def main():
    posts = get_data()
    model,device = initialize_model()
    with open('ids.txt', 'r') as f:
        ids = [line.strip() for line in f]

    new_ids = set()
    for post in posts:
        curid, text, images = post
        if curid not in ids:
            post_embedding = create_embedding(model, device, text, images)
            flattened = flatten_embedding(post_embedding)
            if write_embeddings(flattened):
                new_ids.add(curid)
        else:
            print('duplicate not written')
    with open('ids.txt', 'a') as f:
        for post_id in new_ids:
            f.write(post_id + '\n')

if __name__ == "__main__":
    main()
