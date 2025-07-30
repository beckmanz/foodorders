from flask import Flask
from controllers.pedido_controller import pedido_bp
from controllers.relatorio_controller import relatorio_bp

app = Flask(__name__)
app.register_blueprint(pedido_bp)
app.register_blueprint(relatorio_bp)

app.run(host="localhost", port=5000, debug=True)