from flask import request, Blueprint
from models.pedido_model import Pedido
from services.pedido_service import PedidoService

pedido_bp = Blueprint("pedido", __name__)
service = PedidoService()

@pedido_bp.post("/pedido")
def criar_pedido():
    data = request.json
    pedido = Pedido(
            id_pedido=data["id_pedido"],
            restaurante=data["restaurante"],
            valor=data["valor"],
            tempo_entrega=data["tempo_entrega"],
            status=data["status"],
            cidade=data["cidade"],
            data_hora=data["data_hora"]
        )
    res = service.salvar_pedido(pedido)
    return res