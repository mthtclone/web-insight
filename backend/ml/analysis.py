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
            # DeepGaze outputs log probabilities.
            # Convert them back into probabilities.

            probability_region = np.exp(
                region
            )

            score = float(
                probability_region.mean()
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
            if max_score > 0
            else 0
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
    metrics: dict,
    elements: list
):

    recommendations = []

    cta_visibility = metrics.get(
        "cta_visibility",
        0
    )


    if cta_visibility < 40:

        recommendations.append(
            "Primary CTA receives very low visual attention. Consider increasing button size, improving color contrast, and moving it to a more prominent location."
        )

    elif cta_visibility < 70:

        recommendations.append(
            "CTA visibility is moderate. Consider strengthening visual emphasis through spacing, contrast, typography, or placement improvements."
        )

    headline_prominence = metrics.get(
        "headline_prominence",
        0
    )


    if headline_prominence < 40:

        recommendations.append(
            "The main headline is not attracting enough attention. Consider increasing font size, improving contrast, and positioning it closer to the user's initial viewing area."
        )

    elif headline_prominence < 70:

        recommendations.append(
            "The headline has reasonable visibility but may compete with other elements. Consider reducing distractions around the main message."
        )

    hierarchy = metrics.get(
        "visual_hierarchy",
        0
    )


    if hierarchy < 25:

        recommendations.append(
            "Visual hierarchy is weak. Create stronger differences between primary and secondary elements using size, spacing, contrast, and positioning."
        )

    elif hierarchy < 50:

        recommendations.append(
            "Visual hierarchy can be improved. Consider emphasizing important information while reducing attention given to less important elements."
        )

    overall_score = metrics.get(
        "overall_ux_score",
        0
    )


    if overall_score < 40:

        recommendations.append(
            "The webpage has poor attention distribution. Consider restructuring the layout to guide users toward important content and actions."
        )

    elif overall_score < 70:

        recommendations.append(
            "The webpage has acceptable usability but could benefit from improved attention flow and stronger prioritization of key elements."
        )

    if elements:

        high_attention_elements = [
            element
            for element in elements
            if element.get(
                "attention_percentage",
                0
            ) >= 80
        ]


        if len(high_attention_elements) > 5:

            recommendations.append(
                "Many elements compete for user attention. Consider simplifying the layout and reducing unnecessary visual emphasis."
            )


        elif len(high_attention_elements) == 0:

            recommendations.append(
                "No element strongly attracts attention. Consider introducing stronger visual anchors for important content."
            )


    if elements:

        ctas = [
            element
            for element in elements
            if element.get(
                "is_cta",
                False
            )
        ]


        if ctas:

            highest_attention = max(
                elements,
                key=lambda x:
                    x.get(
                        "attention_percentage",
                        0
                    )
            )


            highest_cta = max(
                ctas,
                key=lambda x:
                    x.get(
                        "attention_percentage",
                        0
                    )
            )


            if highest_attention != highest_cta:

                recommendations.append(
                    "Users may focus on elements other than the primary action. Consider redesigning the CTA to become the strongest visual focus."
                )

    if not recommendations:

        recommendations.append(
            "The webpage has a balanced attention pattern. Continue maintaining clear hierarchy and strong element prioritization."
        )


    return recommendations

def generate_ui_metrics(
    elements: list
):

    metrics = {
        "cta_prominence": 0,
        "headline_prominence": 0,
        "visual_clutter": 0,
        "text_density": 0,
    }


    if not elements:
        return metrics


    # CTA prominence

    ctas = [
        element
        for element in elements
        if element.get("is_cta")
    ]

    if ctas:
        metrics["cta_prominence"] = round(
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


    # Visual clutter

    element_count = len(elements)


    metrics["visual_clutter"] = round(
        min(
            element_count * 5,
            100
        ),
        2
    )


    # Text density

    total_text_length = sum(
        len(
            element.get(
                "text",
                ""
            )
        )
        for element in elements
    )


    metrics["text_density"] = round(
        min(
            total_text_length / 10,
            100
        ),
        2
    )


    return metrics

def generate_findings(
    metrics: dict,
    elements: list
):

    findings = []

    cta_visibility = metrics.get(
        "cta_visibility",
        0
    )


    if cta_visibility >= 80:

        findings.append(
            "The primary CTA receives strong visual attention and is likely easy for users to notice."
        )

    elif cta_visibility >= 50:

        findings.append(
            "The primary CTA receives moderate attention but may benefit from stronger visual emphasis."
        )

    else:

        findings.append(
            "The primary CTA receives limited visual attention and may be overlooked by users."
        )

    headline_prominence = metrics.get(
        "headline_prominence",
        0
    )


    if headline_prominence >= 80:

        findings.append(
            "The main headline successfully captures user attention and establishes strong visual focus."
        )

    elif headline_prominence >= 50:

        findings.append(
            "The main headline is visible but may compete with other webpage elements."
        )

    else:

        findings.append(
            "The main headline does not attract sufficient attention to effectively communicate the primary message."
        )

    hierarchy = metrics.get(
        "visual_hierarchy",
        0
    )


    if hierarchy >= 60:

        findings.append(
            "The webpage demonstrates a strong visual hierarchy, with clear differences between important and secondary elements."
        )

    elif hierarchy >= 30:

        findings.append(
            "The webpage has a moderate visual hierarchy, but some elements may compete for user attention."
        )

    else:

        findings.append(
            "The webpage has weak visual hierarchy, making it harder for users to identify important information."
        )

    overall_score = metrics.get(
        "overall_ux_score",
        0
    )


    if overall_score >= 80:

        findings.append(
            "The webpage has an effective attention distribution that supports user navigation."
        )

    elif overall_score >= 50:

        findings.append(
            "The webpage has an acceptable attention pattern but contains opportunities for visual improvement."
        )

    else:

        findings.append(
            "The webpage has poor attention distribution and may require layout improvements."
        )

    if elements:

        high_attention_elements = [
            element
            for element in elements
            if element.get(
                "attention_percentage",
                0
            ) >= 80
        ]


        if len(high_attention_elements) > 5:

            findings.append(
                "Multiple elements receive high visual attention, which may reduce focus on the most important actions."
            )


        elif len(high_attention_elements) == 1:

            findings.append(
                "The webpage has a clear primary attention target."
            )

    if elements:

        ctas = [
            element
            for element in elements
            if element.get(
                "is_cta",
                False
            )
        ]


        if ctas:

            highest_cta = max(
                ctas,
                key=lambda x:
                    x.get(
                        "attention_percentage",
                        0
                    )
            )


            highest_element = max(
                elements,
                key=lambda x:
                    x.get(
                        "attention_percentage",
                        0
                    )
            )


            if highest_cta != highest_element:

                findings.append(
                    "The highest-attention element is not the primary CTA, which may indicate users are being distracted from the intended action."
                )

            else:

                findings.append(
                    "The primary CTA aligns with the strongest visual attention area."
                )

    if elements:

        low_attention_elements = [
            element
            for element in elements
            if element.get(
                "attention_percentage",
                0
            ) < 20
        ]


        if len(low_attention_elements) > 3:

            findings.append(
                "Several webpage elements receive very low attention and may not effectively communicate their purpose."
            )


    return findings