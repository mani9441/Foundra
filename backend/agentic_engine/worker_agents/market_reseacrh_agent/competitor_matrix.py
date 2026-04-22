def generate_competitor_matrix(data):
    competitors = data.get("competitors", [])

    matrix = []

    for comp in competitors:
        matrix.append({
            "Name": comp.get("name"),
            "Description": comp.get("description"),
            "Strength": comp.get("strength"),
            "Weakness": comp.get("weakness"),
            "Positioning": determine_position(comp)
        })

    return matrix


def determine_position(comp):
    desc = (comp.get("description") or "").lower()

    if "ai" in desc or "automation" in desc:
        return "AI-driven"

    elif "marketplace" in desc or "platform" in desc:
        return "Platform-based"

    elif "subscription" in desc or "saas" in desc:
        return "SaaS"

    elif "hardware" in desc or "device" in desc:
        return "Hardware + Software"

    elif "enterprise" in desc or "b2b" in desc:
        return "B2B Solution"

    elif "consumer" in desc or "app" in desc:
        return "B2C App"

    else:
        return "General Product"