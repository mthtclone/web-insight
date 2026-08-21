from ml.saliency import SaliencyAnalyzer


def main():

    analyzer = SaliencyAnalyzer()

    output = analyzer.generate_overlay(
        "data/screenshots/page.png",
        "data/overlay_test.png"
    )

    print(
        "Generated:",
        output
    )


if __name__ == "__main__":
    main()