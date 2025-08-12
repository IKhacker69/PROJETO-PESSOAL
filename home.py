from flask import Flask, render_template, redirect, request, flash, session, url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='usuarios'

    )

cursor = conexao.cursor(pymysql.cursors.DictCursor)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'INACIO'

cursor = conexao.cursor(pymysql.cursors.DictCursor)


def get_agendamentos():
    cursor.execute('SELECT * FROM agendamentos')
    return cursor.fetchall()


@app.route('/agendamentos')
def teste():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login_page'))
    agendamentos = get_agendamentos()
    return render_template('agendamentos.html', agendamentos=agendamentos)



@app.route('/novo', methods=['get','POST'])
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login_page'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        hora = request.form.get('hora')
        cursor.execute(
            'INSERT INTO agendamentos (nome, categoria, data, hora) VALUES (%s, %s, %s, %s)',
            (nome, categoria, data, hora)
        )
        conexao.commit()
    return render_template ('novo.html')



@app.route('/editar', methods=['POST'])
def editar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login_page'))
    if request.method == 'POST':
        agendamento_id = request.form.get('id')  # Supondo que o ID venha do formulário
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        data = request.form.get('data')
        hora = request.form.get('hora')
        cursor.execute(
            'UPDATE agendamentos SET nome=%s, categoria=%s, data=%s, hora=%s WHERE id=%s',
            (nome, categoria, data, hora, agendamento_id)
        )
        conexao.commit()
    return render_template('editar.html')

@app.route('/atualizar', methods=['POST', 'GET'])
def atualizar():
    pass 


@app.route('/home')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect (url_for('login_page'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        cursor.execute('SELECT id, nome, senha FROM login WHERE nome = %s', (nome,))
        usuario = cursor.fetchone()
        print(usuario)

        
        if usuario and check_password_hash(usuario['senha'], senha): # **Verifica a senha com hash**
            session['usuario_logado'] = usuario['nome'] # **Define a sessão aqui!**
            flash(f'Bem-vindo(a), {usuario["nome"]}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
            return render_template('login.html')
            

    return render_template('login.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrarUsuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        hashed_password = generate_password_hash(senha)
        try:
            # Inserir o NOME e o HASHED_PASSWORD
            cursor.execute('INSERT INTO login (nome, senha) VALUES (%s, %s)', (nome, hashed_password))
            conexao.commit()
            flash('Usuário cadastrado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login_page'))
        except pymysql.Error as e:
            # Lidar com erro de nome de usuário duplicado
            if 'Duplicate entry' in str(e) and 'for key' in str(e): # Mensagem de erro pode variar dependendo do SGBD
                 flash('Este nome de usuário já existe. Por favor, escolha outro.', 'error')
            else:
                 flash(f'Erro ao cadastrar usuário: {e}', 'error')
            conexao.rollback() 
            return render_template('cadastro.html')
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None) # Remove o usuário da sessão
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('login_page'))

    
if __name__ == '__main__':
    app.run(debug=True)