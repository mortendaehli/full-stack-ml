from pathlib import Path

import pytest
from imagenet import ImageNet, __version__
from PIL import Image


def test_version():
    assert __version__ == "0.1.0"


class TestImageNet:
    image_net = ImageNet()

    def test_prediction(self) -> None:
        image_to_predict = Path(__file__).parent / "test_data" / "dog.jpg"
        with Image.open(image_to_predict) as image:
            self.image_net.predict(image=image)

    @pytest.mark.xfail(reason="Not implemented yet.")
    def test_explanation(self) -> None:
        image_to_predict = Path(__file__).parent / "test_data" / "dog.jpg"
        with Image.open(image_to_predict) as image:
            self.image_net.explain(image=image)
