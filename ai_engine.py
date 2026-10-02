def analyze_complaint(text):
    text = text.lower()

    if any(x in text for x in ["wifi", "wi-fi", "internet", "network"]):
        category = "Internet / Wi-Fi"

    elif any(x in text for x in ["projector", "computer", "pc", "laptop", "lab"]):
        category = "Computer / Lab"

    elif any(x in text for x in ["light", "electricity", "fan", "ac", "electric"]):
        category = "Electricity"

    elif any(x in text for x in ["library", "book"]):
        category = "Library"

    elif any(x in text for x in ["hostel", "mess"]):
        category = "Hostel"

    elif any(x in text for x in ["clean", "garbage", "dustbin", "dirty"]):
        category = "Cleanliness"

    elif any(x in text for x in ["class", "classroom"]):
        category = "Classroom"

    else:
        category = "Other"

    if any(x in text for x in ["emergency", "danger", "fire", "shock"]):
        priority = "Emergency"

    elif any(x in text for x in [
        "urgent", "broken", "not working", "cannot", "can't"
    ]):
        priority = "High"

    elif any(x in text for x in ["problem", "issue", "slow"]):
        priority = "Medium"

    else:
        priority = "Low"

    return category, priority