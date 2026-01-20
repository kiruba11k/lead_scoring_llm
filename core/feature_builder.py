class FeatureBuilderLLM:
    """
    This builder prepares clean structured JSON input for Groq LLM scoring.
    No ML model features. Only human-readable structured fields.
    """

    def build_payload(self, linkedin_data: dict, user_data: dict):
        basic = linkedin_data.get("basic_info", {}) if linkedin_data else {}
        exp = linkedin_data.get("experience", []) if linkedin_data else []

        current_role = ""
        current_company = ""
        if isinstance(exp, list):
            for e in exp:
                if e.get("is_current", False):
                    current_role = e.get("title", "") or ""
                    current_company = e.get("company", "") or ""
                    break

        if not current_role:
            current_role = basic.get("headline", "") or ""

        payload = {
            "prospect": {
                "name": basic.get("fullname", ""),
                "headline": basic.get("headline", ""),
                "location": (basic.get("location", {}) or {}).get("full", ""),
                "current_role": current_role,
                "current_company": current_company,
                "activity_days": linkedin_data.get("activity_days", None),
                "recent_posts": linkedin_data.get("recent_posts", []),
            },
            "company_manual": {
                "company_name": user_data.get("company_name", ""),
                "company_size": user_data.get("company_size", ""),
                "annual_revenue": user_data.get("annual_revenue", ""),
                "industry": user_data.get("industry", ""),
            }
        }

        return payload
