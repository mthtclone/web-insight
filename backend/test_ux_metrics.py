from ml.analysis import generate_ux_metrics


def main():

    elements = [

        {
            "tag":"h1",
            "text":"Build faster",
            "attention_percentage":95,
            "is_cta":False
        },

        {
            "tag":"button",
            "text":"Start Free Trial",
            "attention_percentage":80,
            "is_cta":True
        },

        {
            "tag":"img",
            "text":"",
            "attention_percentage":40,
            "is_cta":False
        }

    ]


    metrics = generate_ux_metrics(
        elements
    )


    print(metrics)


if __name__ == "__main__":
    main()