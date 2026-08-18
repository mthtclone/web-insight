import torch
import torchvision
import cv2
import PIL
import numpy as np


def main():
    print("PyTorch version:", torch.__version__)
    print("TorchVision version:", torchvision.__version__)
    print("OpenCV version:", cv2.__version__)
    print("Pillow version:", PIL.__version__)
    print("NumPy version:", np.__version__)

    print("\nCUDA available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        print("Running on CPU")


if __name__ == "__main__":
    main()