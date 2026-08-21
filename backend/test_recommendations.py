from ml.analysis import generate_recommendations


def main():

    metrics = {
        "cta_visibility": 35,
        "headline_prominence": 90,
        "visual_hierarchy": 20,
        "overall_ux_score": 48
    }


    recommendations = generate_recommendations(
        metrics
    )


    for recommendation in recommendations:
        print("-", recommendation)


if __name__ == "__main__":
    main()