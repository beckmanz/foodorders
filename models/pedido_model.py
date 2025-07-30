class Pedido:
    def __init__(self, id_pedido, restaurante, valor, tempo_entrega, status, cidade, data_hora):
        self.id_pedido = id_pedido
        self.restaurante = restaurante
        self.valor = valor
        self.tempo_entrega = tempo_entrega
        self.status = status
        self.cidade = cidade
        self.data_hora = data_hora