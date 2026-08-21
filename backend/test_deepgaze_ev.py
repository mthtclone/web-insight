from ml.saliency import SaliencyAnalyzer


def main():

    analyzer = SaliencyAnalyzer()

    result = analyzer.generate_overlay(
        "data/screenshots/page.png",
        "data/overlay_test.png"
    )

    print(
        "Overlay:",
        result["overlay_path"]
    )

    print(
        "Saliency shape:",
        result["saliency_map"].shape
    )


if __name__ == "__main__":
    main()