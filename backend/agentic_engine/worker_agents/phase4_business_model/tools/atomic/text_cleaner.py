import re


def clean_text(text: str):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keywords(text: str, top_n: int = 15):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in ranked[:top_n]]