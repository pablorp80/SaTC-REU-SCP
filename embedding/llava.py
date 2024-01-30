from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path
from llava.eval.run_llava import eval_model
from PIL import Image

def embed_text_image_pair(model_path, text_prompt, image_path):
    tokenizer, model, image_processor, context_len = load_pretrained_model(
        model_path=model_path,
        model_base=None,
        model_name=get_model_name_from_path(model_path),
        offload_folder='/Users/andrewhamara/llava/offload/'
    )

    image = Image.open(image_path).convert("RGB")
    processed_image = image_processor(image=image, return_tensors="pt").input_values

# Set up arguments for evaluation
    args = type('Args', (), {
        "model_path": model_path,
        "model_base": None,
        "model_name": get_model_name_from_path(model_path),
        "query": text_prompt,
        "conv_mode": None,
        "image_file": processed_image,
        "sep": ",",
        "temperature": 0,
        "top_p": None,
        "num_beams": 1,
        "max_new_tokens": 512
    })()

    # Evaluate the model
    result = eval_model(args)

    return result

# Example usage
model_path = "liuhaotian/llava-v1.5-7b"
text_prompt = "MERCEDES BENZ FACTORY VINTAGE PARTS"
image_path = "/images/test_img_1.jpg"

embedding = embed_text_image_pair(model_path, text_prompt, image_path)
print(embedding)
