from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'avanovalar'
DB_USER = 'postgres'
DB_PASSWORD = '1478963'
SCHEMA_NAME = 'novalarschema'  # Nome do schema

from flask import request

@app.route('/vendedores/<int:idvendedor>', methods=['GET'])
def get_vendedor(idvendedor):
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Consultar o vendedor na tabela vendedores dentro do schema
        cursor.execute(f"SELECT idvendedor, nomevendedor FROM {SCHEMA_NAME}.vendedores WHERE idvendedor = %s", (idvendedor,))

        # Obter o resultado da consulta
        vendedor = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Verificar se o vendedor foi encontrado
        if vendedor:
            return jsonify(vendedor)
        else:
            return jsonify({'error': 'Vendedor não encontrado'}), 404

    except psycopg2.Error as e:
        print("Erro ao consultar o vendedor:", e)
        return jsonify({'error': 'Erro ao consultar o vendedor'}), 500


# Rota para inserir a avaliação na tabela avaliacoes
@app.route('/avaliacoes', methods=['POST'])
def inserir_avaliacao():
    try:
        # Receber os dados da avaliação
        data = request.json
        idvendedor = data['idvendedor']
        avaliacao = data['avaliacao']

        # Registrar a data e horário da avaliação
        data_avaliacao = datetime.now()

        # Conectar ao banco de dados
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Inserir a avaliação na tabela avaliacoes dentro do schema
        cursor.execute(f"INSERT INTO {SCHEMA_NAME}.avaliacoes (idvendedor, avaliacao, dataavaliacao, horarioavaliacao) VALUES (%s, %s, %s, %s)",
                       (idvendedor, avaliacao, data_avaliacao.date(), data_avaliacao.time()))

        # Confirmar a transação
        conn.commit()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Retornar mensagem de sucesso
        return jsonify({'message': 'Avaliação inserida com sucesso'})

    except KeyError:
        return jsonify({'error': 'Dados incompletos'}), 400
    except psycopg2.Error as e:
        print("Erro ao inserir avaliação:", e)
        return jsonify({'error': 'Erro ao inserir a avaliação'}), 500

if __name__ == '__main__':
    app.run(debug=True)
