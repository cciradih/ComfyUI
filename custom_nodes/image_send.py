from PIL import Image
from io import BytesIO
import numpy
import requests

class SendImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "url": ("STRING", {}),
                "key": ("STRING", {}),
                "seed": ("INT", {}),
                "callback": ("STRING", {}),
            },
        }
 
    RETURN_TYPES = ()
 
    FUNCTION = "send_images"
 
    OUTPUT_NODE = True
 
    CATEGORY = "api/image"

    def send_images(self, images, url, key, seed, callback):
        names = []
        for index, image in enumerate(images):
            bytes = BytesIO()
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(numpy.clip(i, 0, 255).astype(numpy.uint8))
            img.save(bytes, format="PNG")
            name = str(seed) + "-" + str(index) + ".png"
            path  = "/" + name
            requests.post(url+path, headers={"key": key}, data=bytes.getvalue())
            names.append(name)
        requests.post(callback, json=names)
        return {}

NODE_CLASS_MAPPINGS = {
    "SendImage": SendImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendImage": "Send Image"
}
