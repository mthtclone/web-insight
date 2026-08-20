import torch
import numpy as np

from ml.preprocess import (
    preprocess_image,
    create_centerbias
)


def main():

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    image = preprocess_image(
        "data/screenshots/page.png",
        device
    )

    _, _, height, width = image.shape

    centerbias = create_centerbias(
        height,
        width,
        device
    )

    print("Image:")
    print(image.shape)

    print("Center bias:")
    print(centerbias.shape)

    print("Device:", image.device)
    print("Shape:", image.shape)


if __name__ == "__main__":
    main()