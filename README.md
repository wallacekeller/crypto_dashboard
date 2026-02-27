# 🚀 Crypto Dashboard

Dashboard de criptomoedas em tempo real direto no terminal, para **BTC** e **ETH**.

```
┌─────────────────────────────────────────────────────────────────────┐
│           🚀 CRYPTO DASHBOARD    27/02/2025  14:32:10               │
└─────────────────────────────────────────────────────────────────────┘

 ╭── ₿ BTC ─────────────────────╮   ╭── Ξ ETH ─────────────────────╮
 │  ₿ BTC   $62,450.00  ▲ 2.3%  │   │  Ξ ETH   $3,120.00  ▼ 0.8%   │
 │                              │   │                              │
 │  Preço USD   $62,450.00      │   │  Preço USD   $3,120.00       │
 │  Preço BRL   R$ 312,250.00   │   │  Preço BRL   R$ 15,600.00    │
 │  Variação    ▲ 2.30%         │   │  Variação    ▼ 0.80%         │
 │  Volume 24h  $28.5B          │   │  Volume 24h  $14.2B          │
 │  Market Cap  $1.22T          │   │  Market Cap  $374.4B         │
 │  ATH         $73,737.00      │   │  ATH         $4,891.00       │
 │  Circulação  19.6M (93.4%)   │   │  Circulação  120.2M          │
 │                              │   │                              │
 │  Últimos 7 dias              │   │  Últimos 7 dias              │
 │  ▃▄▄▅▆▆▇▇▇▇▇▇▇▇█   │   │ ▆▆▆▆▅▅▄▄▃▃▄▄▃▃▃▃▃  │
 ╰──────────────────────────────╯   ╰──────────────────────────────╯

 ┌─ 📊 Comparativo Rápido ──────────────────────────────────────────────┐
 │ Moeda  │      USD      │       BRL       │  24h   │ Volume │ Mkt Cap │
 │ ₿ BTC  │ $62,450.00   │ R$ 312,250.00   │ ▲ 2.3% │ $28.5B │  $1.22T  │
 │ Ξ ETH  │  $3,120.00   │  R$ 15,600.00   │ ▼ 0.8% │ $14.2B │ $374.4B  │
 └──────────────────────────────────────────────────────────────────────┘

  ● Última atualização: 14:32:10   Fonte: CoinGecko API   [Q] sair

```

## ✨ Funcionalidades

- Preços em tempo real em **USD** e **BRL**
- Variação das últimas **24 horas** com indicador visual ▲ ▼
- **Sparkline** dos últimos 7 dias no terminal
- Volume 24h, Market Cap, ATH e supply circulante
- **Tabela comparativa** lado a lado
- Auto-atualização a cada **30 segundos**
- Interface colorida com [Rich](https://github.com/Textualize/rich)
- Dados via **CoinGecko API** (gratuita, sem chave necessária)

## 🛠 Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/crypto-dashboard.git
cd crypto-dashboard

# Crie um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

## ▶️ Uso

```bash
python dashboard.py
```

Pressione `Ctrl+C` para sair.

## 📦 Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| [rich](https://github.com/Textualize/rich) | ≥ 13.0 | Interface do terminal |
| [requests](https://docs.python-requests.org) | ≥ 2.28 | Chamadas à API |

## 🔌 API

Utiliza a [CoinGecko API v3](https://www.coingecko.com/en/api) — **100% gratuita**, sem necessidade de cadastro ou chave de API.

Endpoints utilizados:
- `/simple/price` — preços atuais, variação e volume
- `/coins/{id}/market_chart` — histórico para o sparkline
- `/coins/{id}` — ATH, supply circulante e outros detalhes

## 📁 Estrutura

```
crypto-dashboard/
├── dashboard.py      # Código principal
├── requirements.txt  # Dependências
└── README.md         # Este arquivo
```

## 🤝 Contribuindo

Pull requests são bem-vindos! Algumas ideias de melhoria:

- [ ] Suporte a mais moedas (SOL, BNB, etc.)
- [ ] Alertas de preço configuráveis
- [ ] Exportar histórico para CSV
- [ ] Gráfico de velas (candlestick) no terminal

## 📄 Licença

MIT
