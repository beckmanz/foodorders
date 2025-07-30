import os
import csv
from flask import make_response, jsonify
from models.pedido_model import Pedido

class PedidoService:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.arquivo = "data/pedidos.csv"
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id_pedido", "restaurante", "valor", "tempo_entrega", "status", "cidade", "data_hora"])  