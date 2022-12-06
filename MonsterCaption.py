import re
import torch
from transformers import AutoTokenizer, AutoFeatureExtractor, VisionEncoderDecoderModel

def generateMonsterCaption(monsterImg):

    # Pattern to ignore all the text after 2 or more full stops
    regex_pattern = "[.]{2,}"

    def post_process(text):
        text = text.strip()
        text = re.split(regex_pattern, text)[0]
        return text


    def predict(image, max_length=64, num_beams=4):
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        with torch.no_grad():
            output_ids = model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                return_dict_in_generate=True,
            ).sequences

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        pred = post_process(preds[0])

        return pred

    model_name_or_path = "deepklarity/poster2plot"
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Load model.

    model = VisionEncoderDecoderModel.from_pretrained(model_name_or_path)
    model.to(device)
    print("Loaded model")

    feature_extractor = AutoFeatureExtractor.from_pretrained(model.encoder.name_or_path)
    print("Loaded feature_extractor")

    tokenizer = AutoTokenizer.from_pretrained(model.decoder.name_or_path, use_fast=True)
    if model.decoder.name_or_path == "gpt2":
        tokenizer.pad_token = tokenizer.eos_token

    print("Loaded tokenizer")
    pred = predict(monsterImg)

    return pred
