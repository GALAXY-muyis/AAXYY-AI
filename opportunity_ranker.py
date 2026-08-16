def rank_opportunities(opportunities):
    """
    Rank trading opportunities from strongest to weakest.
    """

    ranked = []

    for opportunity in opportunities:
        score = opportunity.get("score", 0)
        confidence = opportunity.get("confidence", 0)
        risk_reward = opportunity.get("risk_reward", 0)

        volume_status = opportunity.get(
            "volume_status",
            "NORMAL",
        )

        conflict_status = opportunity.get(
            "conflict_status",
            "NONE",
        )

        ranking_score = (
            score * 0.50
            + confidence * 0.25
            + min(risk_reward * 10, 100) * 0.15
        )

        if volume_status == "HIGH":
            ranking_score += 10

        if conflict_status == "CONFLICT":
            ranking_score -= 20

        opportunity_copy = dict(opportunity)

        opportunity_copy["ranking_score"] = round(
            ranking_score,
            2,
        )

        ranked.append(opportunity_copy)

    ranked.sort(
        key=lambda item: item["ranking_score"],
        reverse=True,
    )

    return ranked


def get_best_opportunity(opportunities):
    """
    Return the strongest available opportunity.
    """

    ranked = rank_opportunities(opportunities)

    if not ranked:
        return None

    return ranked[0]
