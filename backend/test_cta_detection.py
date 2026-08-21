from ml.analysis import detect_cta_elements


def main():

    elements = [
        {
            "tag": "button",
            "text": "Start Free Trial"
        },
        {
            "tag": "a",
            "text": "Learn More"
        },
        {
            "tag": "h1",
            "text": "Build faster"
        }
    ]


    results = detect_cta_elements(
        elements
    )


    print(results)


if __name__ == "__main__":
    main()