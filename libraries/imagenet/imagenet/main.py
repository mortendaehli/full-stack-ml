from functools import lru_cache
from io import BytesIO
from typing import Any, Dict, List, Tuple

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.python.keras.backend as K
from fastapi import File
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

tf.compat.v1.disable_eager_execution()


@lru_cache
def load_mobilenetv2():
    """Load pre-trained MobileNetV2 with ImageNet weights."""
    return keras.applications.MobileNetV2(weights="imagenet")


@lru_cache
def load_vgg16():
    """Load pre-trained MobileNetV2 with ImageNet weights."""
    return keras.applications.VGG16(weights="imagenet")


@lru_cache
def get_shap_dataset_imagenet_50() -> Tuple[np.array, np.array]:  # noqa
    """Load sample dataset from Imagenet"""
    """
    return shap.datasets.imagenet50()
    """
    pass


@lru_cache
def get_imagenet_class_names():
    """Load the ImageNet class names"""
    """
    url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
    fname = shap.datasets.cache(url)
    with open(fname) as f:
        class_names = json.load(f)
    return class_names
    """


class ImageNet:
    def __init__(self):
        self.model: keras.Model = load_mobilenetv2()
        # self.model_explainer: Optional[shap.Explainer] = None

    @staticmethod
    def parse_image(file: File) -> Image.Image:
        image = Image.open(BytesIO(file))
        return image

    def predict(self, image: Image.Image) -> List[Dict[str, Any]]:
        # Resizing the image
        image = np.asarray(image.resize((224, 224)))[..., :3]
        image = np.expand_dims(image, 0)
        image = image / 127.5 - 1.0

        # Making prediction
        result = keras.applications.imagenet_utils.decode_predictions(preds=self.model.predict(image), top=2)[0]

        # Adding some context to the result.
        return [{"prediction": x[1], "confidence": x[2]} for x in result]

    def explain(self, image: Image.Image, plot: bool = False) -> Any:
        """
        Fixme:
            There is a change in behaviour in TensorFlow. Need to figure this out or run TF v1.

        :param image: The image we want to explain.
        :param plot: To plot Shap values or not.
        :return:
        """
        """
        image = np.asarray(image.resize((224, 224)))[..., :3]
        image = np.expand_dims(image, 0)
        image = image / 127.5 - 1.0

        X, y = get_shap_dataset_imagenet_50()

        class_names = get_imagenet_class_names()

        if not self.model_explainer:
            self.model_explainer = shap.GradientExplainer(
                model=(self.model.layers[7].input, self.model.layers[-1].output),
                data=self.map2layer(preprocess_input(X.copy()), 7),
            )
        shap_values, indexes = self.model_explainer.shap_values(self.map2layer(image, 7), ranked_outputs=2)

        # get the names for the classes
        index_names = np.vectorize(lambda x: class_names[str(x)][1])(indexes)

        if plot:
            shap.image_plot(shap_values, image, index_names)

        return shap_values, index_names
        """
        pass

    def map2layer(self, x, layer):
        """Explain how the input to the 7th layer of the model explains the top two classes"""
        feed_dict = dict(zip([self.model.layers[0].input], [preprocess_input(x.copy())]))
        return K.get_session().run(self.model.layers[layer].input, feed_dict)
