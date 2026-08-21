import numpy as np


def calculate_element_attention(
    saliency_map: np.ndarray,
    elements: list
):

    results = []

    height, width = saliency_map.shape


    for element in elements:

        x = int(element["x"])
        y = int(element["y"])

        w = int(element["width"])
        h = int(element["height"])


        if w <= 0 or h <= 0:
            continue


        x1 = max(0, x)
        y1 = max(0, y)

        x2 = min(
            width,
            x + w
        )

        y2 = min(
            height,
            y + h
        )


        region = saliency_map[
            y1:y2,
            x1:x2
        ]


        if region.size == 0:
            score = 0

        else:
            score = float(
                region.mean()
            )


        results.append(
            {
                **element,
                "attention_score": score
            }
        )


    return results

def normalize_attention_scores(
    elements: list
):

    if not elements:
        return []


    max_score = max(
        element["attention_score"]
        for element in elements
    )


    if max_score == 0:
        max_score = 1


    ranked_elements = []

    for element in elements:

        normalized = (
            element["attention_score"]
            /
            max_score
        )


        ranked_elements.append(
            {
                **element,

                "attention_percentage":
                    round(
                        normalized * 100,
                        2
                    )
            }
        )


    ranked_elements.sort(
        key=lambda x:
            x["attention_percentage"],
        reverse=True
    )


    for index, element in enumerate(
        ranked_elements
    ):

        element["attention_rank"] = (
            index + 1
        )


    return ranked_elements

def rank_elements(
    elements: list,
    limit: int = 10
):

    ranked = sorted(
        elements,
        key=lambda x: x["attention_percentage"],
        reverse=True
    )

    return ranked[:limit]

def detect_cta_elements(
    elements: list
):

    cta_keywords = [
        "buy",
        "start",
        "signup",
        "sign up",
        "register",
        "download",
        "subscribe",
        "try",
        "get",
        "learn more",
        "contact",
        "book",
        "demo"
    ]


    results = []


    for element in elements:

        tag = element["tag"].lower()

        text = element.get(
            "text",
            ""
        ).lower()


        is_cta = False


        if tag in [
            "button",
            "input"
        ]:
            is_cta = True


        for keyword in cta_keywords:
            if keyword in text:
                is_cta = True


        results.append(
            {
                **element,
                "is_cta": is_cta
            }
        )


    return results

def generate_ux_metrics(
    elements: list
):

    metrics = {
        "cta_visibility": 0,
        "headline_prominence": 0,
        "visual_hierarchy": 0,
        "overall_ux_score": 0
    }


    if not elements:
        return metrics


    # CTA visibility

    ctas = [
        element
        for element in elements
        if element.get("is_cta")
    ]


    if ctas:
        metrics["cta_visibility"] = round(
            max(
                cta["attention_percentage"]
                for cta in ctas
            ),
            2
        )


    # Headline prominence

    headlines = [
        element
        for element in elements
        if element["tag"] in [
            "h1",
            "h2"
        ]
    ]


    if headlines:
        metrics["headline_prominence"] = round(
            max(
                headline["attention_percentage"]
                for headline in headlines
            ),
            2
        )


    # Visual hierarchy
    #
    # Difference between highest and lowest
    # attention elements

    scores = [
        element["attention_percentage"]
        for element in elements
    ]


    if scores:
        metrics["visual_hierarchy"] = round(
            max(scores) - min(scores),
            2
        )


    # Overall UX score

    metrics["overall_ux_score"] = round(
        (
            metrics["cta_visibility"]
            +
            metrics["headline_prominence"]
            +
            metrics["visual_hierarchy"]
        )
        /
        3,
        2
    )


    return metrics

def generate_recommendations(
    metrics: dict
):

    recommendations = []


    # CTA

    if metrics["cta_visibility"] < 50:
        recommendations.append(
            "Primary CTA receives low visual attention. Consider increasing size, contrast, or improving placement."
        )

    elif metrics["cta_visibility"] < 75:
        recommendations.append(
            "CTA visibility is moderate. Consider making the action more visually prominent."
        )


    # Headline

    if metrics["headline_prominence"] < 50:
        recommendations.append(
            "Main headline is not attracting enough attention. Consider improving typography and positioning."
        )


    # Visual hierarchy

    if metrics["visual_hierarchy"] < 30:
        recommendations.append(
            "Visual hierarchy is weak. Important elements may not stand out clearly from secondary content."
        )


    # Overall score

    if metrics["overall_ux_score"] < 50:
        recommendations.append(
            "Overall visual attention distribution is poor. Review layout structure and element prioritization."
        )


    if not recommendations:
        recommendations.append(
            "The webpage has a balanced visual attention pattern."
        )


    return recommendations