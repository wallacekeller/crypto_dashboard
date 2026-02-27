from crypto_dashboard.formatters import fmt_usd, fmt_brl, fmt_change

def test_fmt_usd_bilhao():
    assert fmt_usd(1_500_000_000) == "$1.50B"

def test_fmt_usd_milhao():
    assert fmt_usd(62_450_000) == "$62.45M"

def test_fmt_usd_normal():
    assert fmt_usd(62_450.00) == "$62,450.00"

def test_fmt_brl():
    assert fmt_brl(312_250.00) == "R$ 312,250.00"

def test_fmt_change_positivo():
    result = fmt_change(2.3)
    assert "▲" in result.plain
    assert "2.30" in result.plain

def test_fmt_change_negativo():
    result = fmt_change(-0.8)
    assert "▼" in result.plain