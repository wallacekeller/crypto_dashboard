"""
Crypto Dashboard — BTC & ETH
Terminal dashboard usando Rich + CoinGecko API (gratuita, sem chave)
"""

import time
import sys
from datetime import datetime
from typing import Optional

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.rule import Rule
from rich import box
from rich.style import Style

console = Console()

COINGECKO_URL = "https://api.coingecko.com/api/v3"
COINS = ["bitcoin", "ethereum"]
SYMBOLS = {"bitcoin": "BTC", "ethereum": "ETH"}
ICONS = {"bitcoin": "₿", "ethereum": "Ξ"}
COLORS = {"bitcoin": "bright_yellow", "ethereum": "bright_cyan"}

REFRESH_INTERVAL = 30  # segundos


# ──────────────────────────────────────────────
# API
# ──────────────────────────────────────────────

def fetch_prices() -> Optional[dict]:
    """Busca preço atual, variações e volume."""
    try:
        ids = ",".join(COINS)
        resp = requests.get(
            f"{COINGECKO_URL}/simple/price",
            params={
                "ids": ids,
                "vs_currencies": "usd,brl",
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
                "include_market_cap": "true",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return None


def fetch_history(coin_id: str, days: int = 7) -> Optional[list]:
    """Busca histórico de preços dos últimos N dias."""
    try:
        resp = requests.get(
            f"{COINGECKO_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": days, "interval": "daily"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return [price for _, price in data.get("prices", [])]
    except requests.RequestException:
        return None


def fetch_coin_detail(coin_id: str) -> Optional[dict]:
    """Busca detalhes adicionais do coin."""
    try:
        resp = requests.get(
            f"{COINGECKO_URL}/coins/{coin_id}",
            params={"localization": "false", "tickers": "false", "community_data": "false"},
            timeout=10,
        )
        resp.raise_for_status()
        d = resp.json()
        return {
            "ath": d["market_data"]["ath"]["usd"],
            "atl": d["market_data"]["atl"]["usd"],
            "circulating_supply": d["market_data"]["circulating_supply"],
            "max_supply": d["market_data"]["max_supply"],
        }
    except requests.RequestException:
        return None


# ──────────────────────────────────────────────
# Formatação
# ──────────────────────────────────────────────

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


def sparkline(prices: list, width: int = 20) -> Text:
    """Gera um mini gráfico de linha com caracteres unicode."""
    if not prices or len(prices) < 2:
        return Text("─" * width, style="dim")

    chars = "▁▂▃▄▅▆▇█"
    mn, mx = min(prices), max(prices)
    rng = mx - mn or 1

    # Normaliza para 0–7
    normalized = [int((p - mn) / rng * 7) for p in prices]

    # Interpola para o width desejado
    step = len(normalized) / width
    sampled = [normalized[min(int(i * step), len(normalized) - 1)] for i in range(width)]

    # Coloração: verde se subiu, vermelho se caiu
    color = "green" if prices[-1] >= prices[0] else "red"
    return Text("".join(chars[v] for v in sampled), style=color)


# ──────────────────────────────────────────────
# Componentes visuais
# ──────────────────────────────────────────────

def build_coin_panel(coin_id: str, price_data: dict, history: Optional[list], details: Optional[dict]) -> Panel:
    symbol = SYMBOLS[coin_id]
    icon = ICONS[coin_id]
    color = COLORS[coin_id]
    data = price_data.get(coin_id, {})

    usd = data.get("usd", 0)
    brl = data.get("brl", 0)
    change_24h = data.get("usd_24h_change", 0)
    volume = data.get("usd_24h_vol", 0)
    mktcap = data.get("usd_market_cap", 0)

    # Cabeçalho
    header = Text()
    header.append(f" {icon} {symbol} ", style=f"bold {color} on grey11")
    header.append(f"  {fmt_usd(usd)}", style=f"bold white")
    header.append("  ")
    header.append(fmt_change(change_24h))

    # Tabela de métricas
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column(style="dim", width=18)
    table.add_column(style="white")

    table.add_row("Preço USD", f"[bold]{fmt_usd(usd)}[/bold]")
    table.add_row("Preço BRL", fmt_brl(brl))
    table.add_row("Variação 24h", fmt_change(change_24h))
    table.add_row("Volume 24h", fmt_usd(volume))
    table.add_row("Market Cap", fmt_usd(mktcap))

    if details:
        if details.get("ath"):
            table.add_row("ATH", fmt_usd(details["ath"]))
        if details.get("circulating_supply"):
            supply = details["circulating_supply"]
            max_s = details.get("max_supply")
            supply_str = f"{supply:,.0f}"
            if max_s:
                pct = (supply / max_s) * 100
                supply_str += f" ({pct:.1f}%)"
            table.add_row("Circulação", supply_str)

    # Sparkline
    spark_text = Text()
    spark_text.append("\n  Últimos 7 dias  ", style="dim")
    if history:
        spark_text.append(sparkline(history, width=30))
    else:
        spark_text.append("sem dados", style="dim")

    from rich.console import Group
    content = Group(header, Text(""), table, spark_text)

    return Panel(
        content,
        title=f"[bold {color}]{icon} {symbol}[/bold {color}]",
        border_style=color,
        padding=(1, 2),
    )


def build_header() -> Panel:
    now = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    text = Text(justify="center")
    text.append("🚀 CRYPTO DASHBOARD", style="bold white")
    text.append(f"    {now}", style="dim")
    text.append(f"    atualiza a cada {REFRESH_INTERVAL}s", style="dim")
    return Panel(text, style="grey30", box=box.HORIZONTALS)


def build_comparison_table(price_data: dict) -> Table:
    table = Table(
        title="📊 Comparativo Rápido",
        box=box.ROUNDED,
        border_style="grey50",
        title_style="bold white",
        show_lines=True,
    )

    table.add_column("Moeda", style="bold", justify="center", width=10)
    table.add_column("USD", justify="right", width=16)
    table.add_column("BRL", justify="right", width=18)
    table.add_column("24h", justify="center", width=12)
    table.add_column("Volume", justify="right", width=14)
    table.add_column("Mkt Cap", justify="right", width=14)

    for coin_id in COINS:
        data = price_data.get(coin_id, {})
        symbol = SYMBOLS[coin_id]
        color = COLORS[coin_id]
        change = data.get("usd_24h_change", 0)

        table.add_row(
            f"[{color}]{ICONS[coin_id]} {symbol}[/{color}]",
            fmt_usd(data.get("usd", 0)),
            fmt_brl(data.get("brl", 0)),
            fmt_change(change),
            fmt_usd(data.get("usd_24h_vol", 0)),
            fmt_usd(data.get("usd_market_cap", 0)),
        )

    return table


def build_footer(last_update: str, ok: bool) -> Text:
    text = Text(justify="center")
    if ok:
        text.append("● ", style="green")
        text.append(f"Última atualização: {last_update}  ", style="dim")
    else:
        text.append("● ", style="red")
        text.append("Erro ao buscar dados — verifique sua conexão  ", style="red dim")
    text.append("Fonte: CoinGecko API  ", style="dim")
    text.append(" [Q] sair", style="bold dim")
    return text


# ──────────────────────────────────────────────
# Loop principal
# ──────────────────────────────────────────────

def render(price_data: Optional[dict], histories: dict, details: dict, last_update: str, ok: bool):
    """Monta e retorna o renderizável completo."""
    from rich.console import Group

    if not price_data:
        price_data = {}

    panels = [
        build_coin_panel("bitcoin", price_data, histories.get("bitcoin"), details.get("bitcoin")),
        build_coin_panel("ethereum", price_data, histories.get("ethereum"), details.get("ethereum")),
    ]

    return Group(
        build_header(),
        Text(""),
        Columns(panels, equal=True, expand=True),
        Text(""),
        build_comparison_table(price_data),
        Text(""),
        build_footer(last_update, ok),
    )


def run():
    console.clear()
    console.print(Panel("[bold yellow]Carregando dados...[/bold yellow]", expand=False))

    histories: dict = {}
    details: dict = {}
    last_update = "—"
    ok = False

    # Busca inicial de histórico e detalhes (menos frequente)
    for coin_id in COINS:
        histories[coin_id] = fetch_history(coin_id, days=7)
        details[coin_id] = fetch_coin_detail(coin_id)

    price_data = fetch_prices()
    if price_data:
        ok = True
        last_update = datetime.now().strftime("%H:%M:%S")

    tick = 0

    try:
        with Live(render(price_data, histories, details, last_update, ok),
                  refresh_per_second=1, screen=True, console=console) as live:

            while True:
                time.sleep(1)
                tick += 1

                # Atualiza preços a cada REFRESH_INTERVAL segundos
                if tick % REFRESH_INTERVAL == 0:
                    new_data = fetch_prices()
                    if new_data:
                        price_data = new_data
                        ok = True
                        last_update = datetime.now().strftime("%H:%M:%S")
                    else:
                        ok = False

                    # Atualiza histórico a cada 5 minutos
                    if tick % 300 == 0:
                        for coin_id in COINS:
                            h = fetch_history(coin_id, days=7)
                            if h:
                                histories[coin_id] = h
                            d = fetch_coin_detail(coin_id)
                            if d:
                                details[coin_id] = d

                live.update(render(price_data, histories, details, last_update, ok))

    except KeyboardInterrupt:
        console.clear()
        console.print("[bold yellow]Dashboard encerrado. Até logo! 👋[/bold yellow]")
        sys.exit(0)


if __name__ == "__main__":
    run()