import yfinance as yf
import json
import os
from dash import Dash, dcc, html, Input, Output, State, callback_context

# Perustetaan Dash-sovellus
app = Dash(__name__)

# Tiedostojen nimet
USERS_FILE = "users.json"
STOCKS_FILE = "stocks.json"

# Ladataan käyttäjätiedot
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Ladataan osaketiedot (vain lokikäyttöön tässä sovelluksessa)
if os.path.exists(STOCKS_FILE):
    with open(STOCKS_FILE, "r") as f:
        stocks = json.load(f)
else:
    stocks = {}

# Tallennusfunktiot
def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def save_stocks():
    with open(STOCKS_FILE, "w") as f:
        json.dump(stocks, f)

# Funktion osakekurssien hakemiseksi
def get_stock_data(ticker, period='1y'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    # Tallennetaan hakutiedot
    stocks[ticker] = {
        "last_close": data['Close'].iloc[-1],
        "history": data['Close'].to_dict()
    }
    save_stocks()
    return data

# Funktion osakkeiden ostamiseen
def buy_stock(user, ticker, amount):
    global users
    stock_data = get_stock_data(ticker, period='1d')
    latest_price = stock_data['Close'].iloc[-1]
    total_cost = latest_price * amount
    if users[user]['cash'] >= total_cost:
        users[user]['cash'] -= total_cost
        users[user]['portfolio'][ticker] = users[user]['portfolio'].get(ticker, 0) + amount
        save_users()
        return f"Bought {amount} shares of {ticker}."
    else:
        return "Not enough cash to complete the purchase."

# Funktion osakkeiden myymiseen
def sell_stock(user, ticker, amount):
    global users
    if ticker in users[user]['portfolio'] and users[user]['portfolio'][ticker] >= amount:
        stock_data = get_stock_data(ticker, period='1d')
        latest_price = stock_data['Close'].iloc[-1]
        total_sale = latest_price * amount
        users[user]['portfolio'][ticker] -= amount
        if users[user]['portfolio'][ticker] == 0:
            del users[user]['portfolio'][ticker]
        users[user]['cash'] += total_sale
        save_users()
        return f"Sold {amount} shares of {ticker}."
    else:
        return "Not enough shares to complete the sale."

# Dash-käyttöliittymä
app.layout = html.Div([
    html.H1("Pörssisimulaattori"),
    
    # Käyttäjän valinta tai luonti
    html.Div([
        html.Label("Valitse käyttäjä"),
        dcc.Dropdown(id="user-dropdown", options=[{"label": u, "value": u} for u in users], placeholder="Valitse käyttäjä"),
        html.Label("Tai luo uusi käyttäjä"),
        dcc.Input(id="new-username", type="text", placeholder="Käyttäjän nimi"),
        html.Button("Luo käyttäjä", id="create-user-button"),
        html.Div(id="create-user-result")
    ], style={"marginBottom": "20px"}),

    # Osakekaupat
    html.Div([
        html.Label("Osake"),
        dcc.Input(id="stock-ticker", type="text", placeholder="Esim. AAPL"),
        html.Label("Määrä"),
        dcc.Input(id="stock-amount", type="number", placeholder="Määrä", min=1),
        html.Button("Osta", id="buy-button"),
        html.Button("Myy", id="sell-button"),
        html.Div(id="transaction-result")
    ], style={"marginBottom": "20px"}),

    # Käyttäjän tilitiedot ja graafi
    html.Div([
        html.H2("Käyttäjätili"),
        html.Div(id="user-balance"),
        html.Div(id="user-portfolio")
    ]),
    dcc.Graph(id="portfolio-chart")
])

# Uuden käyttäjän luonti
@app.callback(
    Output("create-user-result", "children"),
    Output("user-dropdown", "options"),
    Input("create-user-button", "n_clicks"),
    State("new-username", "value"),
    prevent_initial_call=True
)
def create_user(n_clicks, username):
    global users
    if not username or username in users:
        return "Käyttäjän luonti epäonnistui. Nimi puuttuu tai on jo käytössä.", [{"label": u, "value": u} for u in users]
    
    # Luodaan uusi käyttäjä
    users[username] = {"cash": 10000.0, "portfolio": {}}
    save_users()
    return f"Käyttäjä {username} luotu.", [{"label": u, "value": u} for u in users]

# Päivitetään käyttäjän tilitiedot
@app.callback(
    Output("user-balance", "children"),
    Output("user-portfolio", "children"),
    Output("transaction-result", "children"),
    Input("buy-button", "n_clicks"),
    Input("sell-button", "n_clicks"),
    State("user-dropdown", "value"),
    State("stock-ticker", "value"),
    State("stock-amount", "value"),
    prevent_initial_call=True
)
def update_user_account(buy_clicks, sell_clicks, user, ticker, amount):
    if not user or not ticker or not amount:
        return "Valitse käyttäjä ja täytä tiedot.", "", ""
    
    ctx = callback_context
    action = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if action == "buy-button":
        result = buy_stock(user, ticker.upper(), amount)
    elif action == "sell-button":
        result = sell_stock(user, ticker.upper(), amount)
    else:
        result = ""
    
    balance = f"Cash: {users[user]['cash']:.2f}"
    portfolio = f"Portfolio: {users[user]['portfolio']}"
    return balance, portfolio, result

# Graafi salkun kehityksestä (yksinkertainen versio)
@app.callback(
    Output("portfolio-chart", "figure"),
    Input("user-dropdown", "value")
)
def update_portfolio_chart(user):
    if not user or user not in users:
        return {"data": [], "layout": {"title": "Ei omistuksia"}}
    
    portfolio = users[user]["portfolio"]
    tickers = list(portfolio.keys())
    if not tickers:
        return {"data": [], "layout": {"title": "Ei omistuksia"}}
    
    values = []
    for ticker in tickers:
        stock_data = get_stock_data(ticker, period='1d')
        latest_price = stock_data['Close'].iloc[-1]
        values.append(latest_price * portfolio[ticker])
    
    return {
        "data": [{"x": tickers, "y": values, "type": "bar", "name": "Portfolio"}],
        "layout": {"title": f"{user}'s Portfolio"}
    }

# Käynnistetään sovellus
if __name__ == "__main__":
    app.run_server(debug=True)
