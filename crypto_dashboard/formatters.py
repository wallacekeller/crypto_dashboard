from rich.text import Text


def fmt_usd(value: float) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value:,.2f}"
    return f"${value:.4f}"


def fmt_brl(value: float) -> str:
    return f"R$ {value:,.2f}"


def fmt_change(change: float) -> Text:
    arrow = "▲" if change >= 0 else "▼"
    color = "green" if change >= 0 else "red"
    return Text(f"{arrow} {abs(change):.2f}%", style=color)