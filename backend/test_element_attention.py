from ml.analysis import (
    calculate_element_attention,
    normalize_attention_scores
)
import numpy as np


def main():

    saliency = np.random.rand(
        2974,
        1440
    )


    elements = [
        {
            "tag": "button",
            "text": "Sign Up",
            "x": 400,
            "y": 500,
            "width": 120,
            "height": 50
        },

        {
            "tag": "h1",
            "text": "Build faster",
            "x": 200,
            "y": 100,
            "width": 500,
            "height": 80
        },

        {
            "tag": "img",
            "text": "",
            "x": 600,
            "y": 300,
            "width": 300,
            "height": 300
        }
    ]


    scores = calculate_element_attention(
        saliency,
        elements
    )

    ranked = normalize_attention_scores(
        scores
    )


    print(ranked)


if __name__ == "__main__":
    main()