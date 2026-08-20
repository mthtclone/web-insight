import torch

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


    print("Inference complete")

    print("Saliency shape:")
    print(saliency.shape)


if __name__ == "__main__":
    main()