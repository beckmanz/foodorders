from flask import jsonify, make_response
import pandas as pd
import os
from datetime import datetime, timedelta
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
    
    def gerar_relatorio_tp_medio_entrega(self, restaurante):
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
        
            def tp_mediod_restaurante(restaurante):
                    pedidos = df[df['restaurante'] == restaurante]
                    if pedidos.empty:
                        return make_response(
                            jsonify({
                                'message': f'Nenhum pedido encontrado para o restaurante: {restaurante}'
                            })
                        ), 404
                    
                    tempo_medio = pedidos['tempo_entrega'].mean()
                    return make_response(
                        jsonify(
                            message=f'Tempo médio de entrega do restaurante calculado com sucesso!',
                            data={
                                'restaurante': restaurante,
                                'tempo_medio': round(tempo_medio, 2)
                            }
                        )
                    ), 200

            if restaurante:
                return tp_mediod_restaurante(restaurante)

            tempo_medio = (
                df.groupby("restaurante")['tempo_entrega']
                    .mean()
                    .reset_index()
                    .to_dict(orient='records')
                    )
            res = make_response(
                jsonify(
                    message='Tempo médio de entrega por restaurante calculado com sucesso!',
                    data=tempo_medio
                )
            ), 200

            return res

        except Exception as e:
            return make_response(
                jsonify({'message': 'Erro ao gerar o relatório.', 'error': str(e)})
            ), 500

    def gerar_relatorio_faturamento(self, inicio, fim):
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
            
            if inicio and fim:
                df['data_hora'] = pd.to_datetime(df['data_hora'])
                df_filtrado = df[(df['data_hora'] >= inicio) & (df['data_hora'] <= fim)]

                fat_total = df_filtrado['valor'].sum()
                
                return make_response(
                    jsonify({
                        "message": "Faturamento por periodo calculado com sucesso!",
                        "data": {
                            "inicio": inicio,
                            "fim": fim,
                            "faturamento_total": fat_total,
                        }
                    }))

            fat = df['valor'].sum()

            res = make_response(
                    jsonify({
                        "message": "Faturamento total calculado com sucesso!",
                        "faturamento_total": fat,
                        }
                    ))
            
            return res
        except Exception as e:
            return make_response(
                jsonify({'message': 'Erro ao gerar o relatório.', 'error': str(e)})
            ), 500

    def gerar_relatorio_pedido_dia(self, cidade, periodo):
        periodo = min(max(1, periodo), 30)
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
            
            df['cidade'] = df['cidade'].str.strip().str.lower()
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            tp_limit = datetime.now() - timedelta(days=periodo) 
            df = df[df['data_hora'] >= tp_limit]

            if cidade:
                df = df[df['cidade'] == cidade.lower().strip()]
            
            pedidos_por_dia = (
                df.groupby(df['data_hora'].dt.date)
                .size()
                .reset_index(name='quantidade_pedidos')
                .rename(columns={"data_hora": 'dia'})
                .to_dict(orient='records')
            )

            res = make_response(
                    jsonify({
                        'message': 'Relatório de pedidos por dia gerado com sucesso!',
                        'data': pedidos_por_dia
                    })), 200
            
            return res
        
        except Exception as e:
            return make_response(
                jsonify({'message': 'Erro ao gerar o relatório.', 'error': str(e)})
            ), 500
