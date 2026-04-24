BENCHMARKS = {
    "saas": {
        "gross_margin": 0.75,
        "ltv_cac_good": 3.0,
        "payback_good_months": 12
    },
    "marketplace": {
        "gross_margin": 0.45,
        "ltv_cac_good": 2.5,
        "payback_good_months": 18
    },
    "ecommerce": {
        "gross_margin": 0.30,
        "ltv_cac_good": 2.0,
        "payback_good_months": 10
    },
    "fintech": {
        "gross_margin": 0.60,
        "ltv_cac_good": 3.0,
        "payback_good_months": 15
    }
}


def get_benchmark(industry: str):
    return BENCHMARKS.get(
        industry.lower(),
        {
            "gross_margin": 0.50,
            "ltv_cac_good": 2.5,
            "payback_good_months": 12
        }
    )