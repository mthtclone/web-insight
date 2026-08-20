# app/ml/preprocess.py

import torch
from PIL import Image
from torchvision import transforms
import numpy as np

def create_centerbias(
        height: int,
        width: int,
        device: torch.device
):
    y, x = np.mgrid[
        0:height,
        0:width
    ]

    center_y = height / 2
    center_x = width / 2

    sigma = min(
        height,
        width
    ) / 3

    centerbias = np.exp(
        -(
            (x - center_x) ** 2
            +
            (y - center_y) ** 2
        )
        /
        (2 * sigma ** 2)
    )

    # Convert to log probability
    centerbias = np.log(
        centerbias
        /
        centerbias.sum()
    )

    centerbias = torch.tensor(
        centerbias,
        dtype=torch.float32
    )

    centerbias = centerbias.unsqueeze(0)

    return centerbias.to(device)

def preprocess_image(
    image_path: str,
    device: torch.device
):
    image = Image.open(image_path).convert("RGB")

    transform = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )

    image_tensor = transform(image)

    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)

    image_tensor = image_tensor.to(device)

    return image_tensor