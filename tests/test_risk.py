from datetime import datetime

from app.risk_analysis import analyze_risk


def test_login_normal():

    result = analyze_risk(
        login_time=datetime(2026, 9, 22, 10, 0),
        usual_start_hour=7,
        usual_end_hour=22,
        country="Brasil",
        usual_country="Brasil",
        known_device=True,
        known_ip=True,
    )

    assert result.level == "BAIXO"
    assert result.score == 0


def test_login_suspeito():

    result = analyze_risk(
        login_time=datetime(2026, 9, 22, 3, 15),
        usual_start_hour=7,
        usual_end_hour=22,
        country="Alemanha",
        usual_country="Brasil",
        known_device=False,
        known_ip=False,
    )

    assert result.level == "ALTO"
    assert result.score == 100