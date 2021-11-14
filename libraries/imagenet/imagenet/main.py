from functools import lru_cache
from io import BytesIO
from typing import Dict, List

import numpy as np
import tensorflow.keras as keras
from fastapi import File
from PIL import Image


@lru_cache
def load_model():
    return keras.applications.MobileNetV2(weights="imagenet")


class ImageNet:
    def __init__(self):
        self.model: keras.Model = load_model()

    @staticmethod
    def parse_image(file: File) -> Image.Image:
        image = Image.open(BytesIO(file))
        return image

    def predict(self, image: Image.Image) -> List[Dict[str, str]]:
        image = np.asarray(image.resize((224, 224)))[..., :3]
        image = np.expand_dims(image, 0)
        image = image / 127.5 - 1.0

        result = keras.applications.imagenet_utils.decode_predictions(self.model.predict(image), 2)[0]

        response = []
        for i, res in enumerate(result):
            resp = {}
            resp["class"] = res[1]
            resp["confidence"] = f"{res[2] * 100:0.2f} %"

            response.append(resp)

        return response
