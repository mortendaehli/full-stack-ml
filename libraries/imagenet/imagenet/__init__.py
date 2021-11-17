__version__ = "0.1.0"
import os

from .main import ImageNet, load_mobilenetv2

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
