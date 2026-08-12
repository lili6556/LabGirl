from flask import Flask, render_template
from chat_cientistas import chat_bp

app = Flask(__name__)

# registra o blueprint do chat
app.register_blueprint(chat_bp)

# Página Inicial
@app.route("/")
def index():
    return render_template("index.html")


# Página 2 - Globo Interativo
@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


# Página 3 - Escolha do Estado
@app.route("/estados")
def estados():
    return render_template("estados.html")


# Página 4 - Cientistas
@app.route("/cientistas")
def cientistas():
    return render_template("cientistas.html")


# Página 5 - Menu Principal
@app.route("/menu")
def menu():
    return render_template("menu.html")


# Página 6 - Elenco de Cientistas
@app.route("/elenco")
def elenco():
    return render_template("elenco.html")


# Página 7 - Chat das Cientistas
@app.route("/chat")
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(debug=True)