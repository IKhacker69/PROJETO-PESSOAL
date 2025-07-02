from flask import Flask, render_template, redirect, request, flash
import pymysql

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
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        cursor.execute('SELECT * FROM login WHERE nome = %s AND senha = %s', (nome, senha))
        usuario = cursor.fetchone()
        print(usuario)

        # if nome == 'Admin' and senha == '123456':
        #     return redirect('/admin')

        if usuario:
            return redirect('/home')
        else:
            flash('Usuário ou senha inválidos!')
            return redirect('/login')
            

    return render_template('login.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrarUsuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        cursor.execute('INSERT INTO login  (nome, senha) VALUES (%s, %s)', (nome, senha))
        conexao.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect('/login')
    else:
        flash('Preencha os campos para cadastrar um novo usuário.')
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
