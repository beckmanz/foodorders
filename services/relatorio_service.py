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
    
    def gerar_relatorio_ticket_medio(self, cidade):
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
            
            def ticket_cidade(cidade):
                pedidos = df[df['cidade'] == cidade]
                if pedidos.empty:
                    return make_response(
                        jsonify({
                            'message': f'Nenhum pedido encontrado para a cidade: {cidade}'
                        })
                    ), 404
                
                ticket_medio = pedidos['valor'].mean()
                return make_response(
                    jsonify(
                        message=f'Ticket médio da cidade calculado com sucesso!',
                        data={
                            'cidade': cidade,
                            'ticket_medio': round(ticket_medio, 2)
                        }
                    )
                ), 200
            
            if cidade:
                return ticket_cidade(cidade)

            ticket = (
                df.groupby("cidade")['valor']
                    .mean()
                    .reset_index()
                    .to_dict(orient='records')
                    )
            res = make_response(
                jsonify(
                    message='Ticket médio por cidade calculado com sucesso!',
                    data=ticket
                )
            ), 200

            return res
        except Exception as e:
            return make_response(
                jsonify({'message': 'Erro ao gerar o relatório.', 'error': str(e)})
            ), 500