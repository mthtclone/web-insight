import torch
from deepgaze_pytorch.deepgaze3 import DeepGazeIII


def main():
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Using device:", device)

    model = DeepGazeIII(
        pretrained=True
    )

    model.to(device)

    model.eval()

    print("DeepGazeIII loaded successfully")


if __name__ == "__main__":
    main()