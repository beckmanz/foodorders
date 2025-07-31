from flask import Blueprint, request
from services.relatorio_service import RelatorioService

relatorio_bp = Blueprint("ralatorio", __name__)
service = RelatorioService()

@relatorio_bp.get('/relatorio/top-restaurantes')
def get_top_restaurantes():
    quantidade = request.args.get('quantidade', default=10, type=int)
    res = service.gerar_relatorio_top_restaurante(quantidade)
    return res