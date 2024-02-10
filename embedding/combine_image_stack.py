from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import pandas as pd
import os
import random
from parsing.parse_craigslist import get_image_file_names

def create_embedding(model, device, text, images):

    images = ['.assets/images/' + image for image in images]
    inputs = {
        ModalityType.VISION : data.load_and_transform_vision_data(images, device),
        ModalityType.TEXT : data.load_and_transform_text([text], device)
    }
    with torch.no_grad():
        embedding = model(inputs)

    image_embedding = embedding[ModalityType.VISION]
    image_embedding_avg = torch.mean(image_embedding, dim=0)
    text_embedding = embedding[ModalityType.TEXT]

    combined_embedding_average = (image_embedding_avg + text_embedding) / 2
    return combined_embedding_average


def flatten_embedding(embedding):
    flattened_tensor = embedding.cpu().numpy().flatten()
    return flattened_tensor

def write_embedding(flattened_embedding):
    try:
        flattened_embedding_reshaped = flattened_embedding.reshape(1, -1)
        embeddings_df = pd.DataFrame(flattened_embedding_reshaped) # create pandas dataframe
        csv_file_path = 'embeddings.csv'
        write_header = not os.path.exists(csv_file_path) # don't write header every time...
        embeddings_df.to_csv(csv_file_path, mode='a', index=False, header=write_header)
        print(f"Embedding written to {csv_file_path}")
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
        if len(image_paths) > 0:
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
            if write_embedding(flattened):
                new_ids.add(curid)
        else:
            print('duplicate not written')
    with open('ids.txt', 'a') as f:
        for post_id in new_ids:
            f.write(post_id + '\n')

if __name__ == "__main__":
    main()
