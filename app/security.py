def determine_action(risk_level: str) -> str:

    actions = {
        "BAIXO": "PERMITIR",
        "MEDIO": "ALERTAR",
        "ALTO": "BLOQUEAR",
    }

    return actions.get(risk_level, "ALERTAR")


def action_description(
    action: str,
    risk_level: str,
    score: int,
) -> str:

    if action == "PERMITIR":
        return (
            f"Acesso permitido. "
            f"Risco {risk_level}, pontuação {score}."
        )

    if action == "ALERTAR":
        return (
            f"Acesso permitido com alerta. "
            f"Risco {risk_level}, pontuação {score}."
        )

    if action == "BLOQUEAR":
        return (
            f"Acesso bloqueado preventivamente. "
            f"Risco {risk_level}, pontuação {score}."
        )

    return "Ação de segurança registrada."