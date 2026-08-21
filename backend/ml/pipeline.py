import torch

from ml.preprocess import preprocess_image, create_centerbias
from ml.saliency import generate_saliency
from ml.analysis import (
    calculate_element_attention,
    normalize_attention_scores,
    rank_elements,
    detect_cta_elements,
    generate_ux_metrics,
    generate_recommendations,
)


class UXAnalyzer:

    def __init__(self):

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = None


    def load_model(self):

        from deepgaze_pytorch.deepgaze3 import DeepGazeIII

        self.model = DeepGazeIII(
            pretrained=True
        )

        self.model.to(
            self.device
        )

        self.model.eval()


    def analyze(
        self,
        screenshot_path,
        elements
    ):

        if self.model is None:
            self.load_model()


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
                width/2,
                width/2,
                width/2,
                width/2
            ]],
            dtype=torch.float32,
            device=self.device
        )


        y_hist = torch.tensor(
            [[
                height/2,
                height/2,
                height/2,
                height/2
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

        return saliency