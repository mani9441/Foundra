# ============================================================
# File: phase5_product_strategy/tools/atomic/tech_stack_lookup_tool.py
# Smart Stack Recommendation Tool
# ============================================================

def tech_stack_lookup(
    budget_level: str,
    speed_priority: bool = True,
    ai_needed: bool = False
):
    stack = {
        "frontend": "Next.js",
        "backend": "FastAPI",
        "database": "PostgreSQL",
        "hosting": "Railway",
        "auth": "Clerk"
    }

    if budget_level == "very_low":
        stack["hosting"] = "Render Free / Railway Starter"

    if ai_needed:
        stack["vector_db"] = "Qdrant"
        stack["queue"] = "Redis"

    if not speed_priority:
        stack["backend"] = "Django"

    return stack