from flask import jsonify, make_response
import pandas as pd
import os
CSV_PATH = 'data/pedidos.csv'

class RelatorioService:
    def gerar_relatorio_top_restaurante(self, quantidade):
        quantidade = min(max(1, quantidade), 100)

        if not os.path.exists(CSV_PATH):
            return make_response(
                jsonify({'message': 'Nenhum pedido registrado ainda.'})
            ), 404
        
        try:
            df = pd.read_csv(CSV_PATH, encoding="latin-1")
            if df.empty:
                return make_response(
                    jsonify({'message': 'Nenhum pedido registrado ainda.'})
                ), 404

            ranking = (
                df['restaurante']
                .value_counts()
                .head(quantidade)
                .reset_index()
                .rename(columns={
                    'restaurante': 'nome_restaurante',
                    'count': 'quantidade_pedidos'
                })
                .to_dict(orient='records')
            )

            res = make_response(
                    jsonify({
                    'message': 'Ranking de restaurantes gerado com sucesso!',
                    'data': ranking
                })
            )

            return res, 200
        except Exception as e:
            return make_response(
                jsonify({'message': 'Erro ao gerar o relatório.', 'error': str(e)})
            ), 500
    