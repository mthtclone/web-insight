import torch
import numpy as np
from PIL import Image
import cv2

from deepgaze_pytorch.deepgaze3 import DeepGazeIII

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

    print("Device:", device)

    print("Loading DeepGazeIII...")

    model = DeepGazeIII(
        pretrained=True
    )

    model.to(device)
    model.eval()

    print("Model loaded")


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


    print("Running inference...")

    x_hist = torch.tensor(
        [[
            width / 2,
            width / 2,
            width / 2,
            width / 2
        ]],
        dtype=torch.float32,
        device=device
    )

    y_hist = torch.tensor(
        [[
            height / 2,
            height / 2,
            height / 2,
            height / 2
        ]],
        dtype=torch.float32,
        device=device
    )


    with torch.no_grad():

        saliency = model(
            image,
            centerbias,
            x_hist=x_hist,
            y_hist=y_hist
        )

        # Remove unnecessary dimensions (1,1,900,1440) -> (900,1440)
        saliency = saliency.squeeze()

        print("Processed saliency shape:")
        print(saliency.shape)

        # CPU numpy

        saliency_np = saliency.cpu().numpy()
        print(type(saliency_np))
        print(saliency_np.shape)


        # Normalize saliency values (log probability map)

        saliency_min = saliency_np.min()
        saliency_max = saliency_np.max()

        saliency_norm = (
            saliency_np - saliency_min
        ) / (
            saliency_max - saliency_min
        )

        saliency_image = (
            saliency_norm * 255
        ).astype(np.uint8)


        Image.fromarray(
            saliency_image
        ).save(
            "data/saliency_raw.png"
        )

        heatmap = cv2.applyColorMap(
            saliency_image,
            cv2.COLORMAP_JET
        )

        screenshot = cv2.imread(
            "data/screenshots/page.png"
        )

        cv2.imwrite(
            "data/heatmap.png",
            heatmap
        )

        print("Screenshot:", screenshot.shape)
        print("Heatmap:", heatmap.shape)

        overlay = cv2.addWeighted(
            screenshot,
            0.6,
            heatmap,
            0.4,
            0
        )

        cv2.imwrite(
            "data/overlay.png",
            overlay
        )

    print("Inference complete")

    print("Saliency shape:")
    print(saliency.shape)


if __name__ == "__main__":
    main()