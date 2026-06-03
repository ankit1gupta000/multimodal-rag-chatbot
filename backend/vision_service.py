from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def describe_image(image):
    inputs = processor(
        image,
        return_tensors="pt"
    )

    output = model.generate(
        **inputs,
        max_new_tokens=100
    )

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption