from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType
import pandas as pd
import os
from parsing.parse_craigslist import get_image_file_names

def create_embedding(model, device, text, images):

#    print('Creating embedding for post:  \n')
#    print(text + '\n')
#    for image in images:
#        print(image)
    images = ['.assets/images/' + image for image in images]
    inputs = {
        ModalityType.VISION : data.load_and_transform_vision_data(images, device),
        ModalityType.TEXT : data.load_and_transform_text([text], device) # TODO discuss this
    }
    with torch.no_grad():
        embedding = model(inputs)

    image_embedding = embedding[ModalityType.VISION]
    image_embedding_avg = torch.mean(image_embedding, dim=0)
    text_embedding = embedding[ModalityType.TEXT]

    combined_embedding_average = (image_embedding_avg + text_embedding) / 2
    return combined_embedding_average

def flatten_reshape_embedding(embedding):
    flattened_tensor = embedding.cpu().numpy().flatten()
    reshaped_flattened_tensor = flattened_tensor.reshape(1, -1)
    return reshaped_flattened_tensor

def write_embedding(flattened_embedding):
    try:
        embeddings_df = pd.DataFrame(flattened_embedding) # create pandas dataframe
        csv_file_path = 'new_embeddings.csv'
        write_header = not os.path.exists(csv_file_path) # don't write header every time...
        embeddings_df.to_csv(csv_file_path, mode='a', index=False, header=write_header)
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
    posts = posts[2500:3000]
    model,device = initialize_model()
    with open('new_ids.txt', 'r') as f:
        ids = [line.strip() for line in f]

    posted = 0
    for post in posts:
        curid, text, images = post
        if curid not in ids:
            post_embedding = create_embedding(model, device, text, images)
            flattened = flatten_reshape_embedding(post_embedding)
            if write_embedding(flattened):
                posted += 1
                print(posted)
                with open('new_ids.txt', 'a') as f:
                    f.write(curid + '\n')
        else:
            print('duplicate not written')

if __name__ == "__main__":
    main()
