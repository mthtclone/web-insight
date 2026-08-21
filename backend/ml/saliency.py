import torch
import numpy as np
import cv2

from deepgaze_pytorch.deepgaze3 import DeepGazeIII

from ml.preprocess import (
    preprocess_image,
    create_centerbias
)


class SaliencyAnalyzer:

    def __init__(self):

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        print(
            "Loading DeepGazeIII on",
            self.device
        )

        self.model = DeepGazeIII(
            pretrained=True
        )

        self.model.to(
            self.device
        )

        self.model.eval()

        print(
            "DeepGazeIII loaded"
        )


    def generate_saliency(
        self,
        screenshot_path: str
    ):

        image = preprocess_image(
            screenshot_path,
            self.device
        )


        _, _, height, width = image.shape


        centerbias = create_centerbias(
            height,
            width,
            self.device
        )


        x_hist = torch.tensor(
            [[
                width / 2,
                width / 2,
                width / 2,
                width / 2
            ]],
            dtype=torch.float32,
            device=self.device
        )


        y_hist = torch.tensor(
            [[
                height / 2,
                height / 2,
                height / 2,
                height / 2
            ]],
            dtype=torch.float32,
            device=self.device
        )


        with torch.no_grad():

            saliency = self.model(
                image,
                centerbias,
                x_hist=x_hist,
                y_hist=y_hist
            )


        saliency = saliency.squeeze()


        return (
            saliency
            .cpu()
            .numpy()
        )



    def generate_overlay(
        self,
        screenshot_path: str,
        saliency_map: np.ndarray,
        output_path: str
    ):


        saliency_norm = (
            saliency_map - saliency_map.min()
        ) / (
            saliency_map.max()
            -
            saliency_map.min()
        )


        saliency_image = (
            saliency_norm * 255
        ).astype(
            np.uint8
        )


        heatmap = cv2.applyColorMap(
            saliency_image,
            cv2.COLORMAP_JET
        )


        screenshot = cv2.imread(
            screenshot_path
        )


        overlay = cv2.addWeighted(
            screenshot,
            0.6,
            heatmap,
            0.4,
            0
        )


        cv2.imwrite(
            output_path,
            overlay
        )


        return output_path