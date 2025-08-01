from flask import Blueprint, request
from services.relatorio_service import RelatorioService

relatorio_bp = Blueprint("ralatorio", __name__)
service = RelatorioService()

@relatorio_bp.get('/relatorio/top-restaurantes')
def get_top_restaurantes():
    quantidade = request.args.get('quantidade', default=10, type=int)
    res = service.gerar_relatorio_top_restaurante(quantidade)
    return res

@relatorio_bp.get('/relatorio/ticket-medio')
def get_ticket_medio():
    cidade = request.args.get('cidade', type=str)
    res = service.gerar_relatorio_ticket_medio(cidade)
    return res

@relatorio_bp.get('/relatorio/tempo-entrega')
def get_tp_medio_entrega():
    restaurante = request.args.get('restaurante', type=str)
    res = service.gerar_relatorio_tp_medio_entrega(restaurante)
    return res

@relatorio_bp.get('/relatorio/faturamento')
def get_faturamento():
    inicio = request.args.get('inicio', type=str)
    fim = request.args.get('fim', type=str)
    res = service.gerar_relatorio_faturamento(inicio, fim)
    return res

@relatorio_bp.get('/relatorio/pedidos-por-dia')
def get_pedidos_dia():
    cidade = request.args.get('cidade', type=str)
    periodo = request.args.get('periodo', default=7, type=int)
    res = service.gerar_relatorio_pedido_dia(cidade, periodo)
    return res
