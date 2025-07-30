from flask import Flask
from controllers.pedido_controller import pedido_bp

app = Flask(__name__)
app.register_blueprint(pedido_bp)
app.run(host="localhost", port=5000, debug=True)