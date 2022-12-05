import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

#input image is a pil image
#description text is a string
#returns new image
def ImageGeneration(inputImage, descriptionText):
    #print(descriptionText)
    #make the size at least 512x512, and if its bigger then make it a multiple of 64
    h = inputImage.height
    w = inputImage.width
    if h < 512 or w < 512:
        reSizedImg = inputImage.resize((512, 512))
    else:
        h += 32
        w += 32
        h = int(h / 64)
        h = h * 64
        w = int(w / 64)
        w = w * 64
        reSizedImg = inputImage.resize((w, h))

    #dreamstudio key, replace if needed, unlikely as Ive used less than 5% of my tokens
    stability_api = client.StabilityInference(key='sk-BmX425SvyQz6eNxEAu9BUIqZmm2wBWg36ofErnliaAS9B8UF', verbose=True)
    answers = stability_api.generate(prompt= descriptionText, init_image=reSizedImg, start_schedule=0.5, steps=20)
    cantShow = False
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed at .5."
                    "trying again with different parameters")
                cantShow = True
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))

    #if it couldnt show try again with more emphasis on the  prompt as that seems to help
    if cantShow:
        answers = stability_api.generate(prompt=descriptionText, init_image=reSizedImg, start_schedule=0.75, steps=20)
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                    cantShow = True
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
    #img.show()
    return img