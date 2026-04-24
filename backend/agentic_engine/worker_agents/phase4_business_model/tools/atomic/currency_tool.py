RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
    "GBP": 0.79
}


def convert_currency(amount: float, from_code="USD", to_code="USD"):
    from_rate = RATES.get(from_code.upper(), 1.0)
    to_rate = RATES.get(to_code.upper(), 1.0)

    usd = amount / from_rate
    converted = usd * to_rate

    return round(converted, 2)