from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_security import roles_required, current_user
import psycopg2
import bcrypt 
import logging


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app = Flask(__name__)
CORS(app)

# Configuração do banco de dados PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'avanovalar'
DB_USER = 'postgres'
DB_PASSWORD = '1478963'
SCHEMA_NAME = 'novalarschema'  # Nome do schema


#rota consultar usuario por id

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def consultar_usuario_por_id(id_usuario):
    try:
        with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {SCHEMA_NAME}.usuarios WHERE idusuario = %s", (id_usuario,))
                usuario = cursor.fetchone()
                if usuario:
                    return jsonify(usuario)
                else:
                    return jsonify({'error': 'Usuário não encontrado'}), 404
    except psycopg2.Error as e:
        print("Erro ao consultar o usuário por ID:", e)
        return jsonify({'error': 'Erro ao consultar o usuário por ID'}), 500



#ROTA BUSCA TODOS USUARIOS
@app.route('/usuarios', methods=['GET'])
def consultar_usuarios():
    try:
        nome = request.args.get('nome')
        if nome:
            with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {SCHEMA_NAME}.usuarios WHERE nome = %s", (nome,))
                    usuarios = cursor.fetchall()
                    if usuarios:
                        return jsonify(usuarios)
                    else:
                        return jsonify({'error': 'Nenhum usuário encontrado com esse nome'}), 404
        else:
            with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {SCHEMA_NAME}.usuarios")
                    usuarios = cursor.fetchall()
                    if usuarios:
                        return jsonify(usuarios)
                    else:
                        return jsonify({'message': 'Nenhum usuário encontrado'}), 404
    except psycopg2.Error as e:
        print("Erro ao consultar os usuários:", e)
        return jsonify({'error': 'Erro ao consultar os usuários'}), 500
    
    
# ROTA CRIAR USUARIO
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    try:
        # Obtenha os dados do novo usuário a partir do corpo da solicitação
        dados_usuario = request.json

        # Valide os dados recebidos

        # Hash da senha antes de armazenar no banco de dados
        senha_hash = bcrypt.hashpw(dados_usuario['senha'].encode('utf-8'), bcrypt.gensalt())

        # Conectar ao banco de dados
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Execute a inserção do novo usuário
        cursor.execute(f"INSERT INTO {SCHEMA_NAME}.usuarios (nome, email, senha, tipo_usuario, ativo, idfilial, grupo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (dados_usuario['nome'], dados_usuario['email'], senha_hash, dados_usuario['tipo_usuario'], True, dados_usuario['idfilial'], dados_usuario['grupo']))
        conn.commit()

        # Feche a conexão com o banco de dados
        cursor.close()
        conn.close()

        # Log do evento de criação de usuário
        logging.info('Novo usuário criado: %s', dados_usuario['email'])

        # Retorne a resposta de sucesso
        return jsonify({'message': 'Usuário criado com sucesso'}), 201

    except psycopg2.Error as e:
        # Log do erro ao criar usuário
        logging.error('Erro ao criar o usuário: %s', e)
        return jsonify({'error': 'Erro ao criar o usuário'}), 500


# ROTA ATUALIZAR USUARIO
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
#@roles_required('admin')  ## LEMBRAR DE ATIVAR AQUI QUANDO REQUERIR USUARIO ADMIN PARA PODER ATUALIZAR
def atualizar_usuario(id_usuario):
    try:
        # Obtenha os dados atualizados do usuário a partir do corpo da solicitação
        dados_atualizados = request.json

        # Conectar ao banco de dados
        with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
            with conn.cursor() as cursor:
                # Execute a atualização dos dados do usuário
                cursor.execute(f"UPDATE {SCHEMA_NAME}.usuarios SET nome = %s, email = %s, senha = %s, tipo_usuario = %s, ativo = %s, idfilial = %s, grupo = %s WHERE idusuario = %s",
                               (dados_atualizados['nome'], dados_atualizados['email'], dados_atualizados['senha'], dados_atualizados['tipo_usuario'], True, dados_atualizados['idfilial'], dados_atualizados['grupo'], id_usuario))
                # Verifique se algum registro foi atualizado
                if cursor.rowcount > 0:
                    # Commit da transação
                    conn.commit()
                    # Retorne a resposta de sucesso
                    return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
                else:
                    # Retorne uma mensagem indicando que o usuário não foi encontrado
                    return jsonify({'error': 'Usuário não encontrado'}), 404

    except psycopg2.Error as e:
        print("Erro ao atualizar o usuário:", e)
        return jsonify({'error': 'Erro ao atualizar o usuário'}), 500




##ROTA DELETAR USUARIO
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
##@roles_required('admin')  ## LEMBRAR DE ATIVAR AQUI QUANDO REQUERIR USUARIO ADMIN PARA PODER CRIAR E TAL
def deletar_usuario(id_usuario):  
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Execute a exclusão do usuário
        cursor.execute(f"DELETE FROM {SCHEMA_NAME}.usuarios WHERE idusuario = %s", (id_usuario,))
        conn.commit()

        # Verifique se algum registro foi excluído
        if cursor.rowcount > 0:
            # Feche a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Retorne a resposta de sucesso
            return jsonify({'message': 'Usuário excluído com sucesso'}), 200
        else:
            # Feche a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Retorne uma mensagem indicando que o usuário não foi encontrado
            return jsonify({'error': 'Usuário não encontrado'}), 404

    except psycopg2.Error as e:
        print("Erro ao deletar o usuário:", e)
        return jsonify({'error': 'Erro ao deletar o usuário'}), 500


#ROTA DESATIVAR USUARIO

@app.route('/usuarios/<int:id_usuario>/desativar', methods=['PUT'])
def desativar_usuario(id_usuario):
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Execute a atualização da coluna 'ativo' para False
        cursor.execute(f"UPDATE {SCHEMA_NAME}.usuarios SET ativo = False WHERE idusuario = %s", (id_usuario,))
        conn.commit()

        # Verifique se algum registro foi atualizado
        if cursor.rowcount > 0:
            # Feche a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Retorne a resposta de sucesso
            return jsonify({'message': 'Usuário desativado com sucesso'}), 200
        else:
            # Feche a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Retorne uma mensagem indicando que o usuário não foi encontrado
            return jsonify({'error': 'Usuário não encontrado'}), 404

    except psycopg2.Error as e:
        print("Erro ao desativar o usuário:", e)
        return jsonify({'error': 'Erro ao desativar o usuário'}), 500

# Função para verificar as credenciais do usuário durante o login
def verificar_credenciais(email, senha):
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {SCHEMA_NAME}.usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    if usuario:
        # Verifique se a senha fornecida coincide com o hash da senha armazenada no banco de dados
        if bcrypt.checkpw(senha.encode('utf-8'), usuario[3].encode('utf-8')):
            return usuario
    return None

# Rota para lidar com solicitações de login
@app.route('/login', methods=['POST'])
@cross_origin()  # Permitindo solicitações CORS para esta rota específica
def login():
    try:
        if request.method == 'POST':
            # Obtenha os dados do usuário do corpo da solicitação
            dados_login = request.json

            # Verifique as credenciais do usuário (substitua por sua própria lógica)
            if 'email' in dados_login and 'senha' in dados_login:
                # Aqui você pode fazer a verificação do usuário e da senha
                # Se as credenciais estiverem corretas, registre o login bem-sucedido no log
                logging.info('Login bem-sucedido para o usuário: %s', dados_login['email'])
                return jsonify({'message': 'Login bem-sucedido'}), 200
            else:
                # Se as credenciais estiverem incorretas, registre o erro no log e retorne uma mensagem de erro
                logging.error('Credenciais incorretas')
                return jsonify({'error': 'Credenciais incorretas'}), 401
        else:
            # Se a rota não estiver configurada para aceitar solicitações POST,
            # registre o erro no log e retorne um erro indicando que o método não é permitido
            logging.error('Método não permitido')
            return jsonify({'error': 'Método não permitido'}), 405

    except Exception as e:
        # Em caso de erro durante o login, registre o erro no log e retorne um erro interno do servidor
        logging.error('Erro durante o login: %s', e)
        return jsonify({'error': 'Erro interno do servidor'}), 500
if __name__ == '__main__':
    app.run(debug=True)

