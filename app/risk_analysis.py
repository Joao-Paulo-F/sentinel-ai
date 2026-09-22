from dataclasses import dataclass
from datetime import datetime


@dataclass
class RiskResult:
    score: int
    level: str
    reasons: list[str]


def analyze_risk(
    login_time: datetime,
    usual_start_hour: int,
    usual_end_hour: int,
    country: str,
    usual_country: str,
    known_device: bool,
    known_ip: bool,
) -> RiskResult:

    score = 0
    reasons = []

    # Horário fora do padrão
    if not (usual_start_hour <= login_time.hour <= usual_end_hour):
        score += 25
        reasons.append("Login fora do horário habitual")

    # País diferente do habitual
    if country.lower() != usual_country.lower():
        score += 35
        reasons.append("País diferente do padrão do usuário")

    # Dispositivo desconhecido
    if not known_device:
        score += 20
        reasons.append("Dispositivo não reconhecido")

    # IP desconhecido
    if not known_ip:
        score += 20
        reasons.append("IP não reconhecido")

    # Classificação
    if score >= 70:
        level = "ALTO"
    elif score >= 40:
        level = "MEDIO"
    else:
        level = "BAIXO"

    return RiskResult(
        score=score,
        level=level,
        reasons=reasons,
    )