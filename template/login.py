from flask import Flask, render_template, redirect, request, flash
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'INACIO'

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
            for usuario in usuarios:
                if nome == 'Admin' and senha == '123456':
                    return redirect('/admin')
                if usuario['nome'] == nome and usuario['senha'] == senha:
                    return redirect('/home')
            flash('Usuário ou senha incorretos!')
            return redirect('/login')

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = [ ]
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            'nome': nome,
            'senha': senha
        }
    ]
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
    
    usuarioNovo = user + usuarios

    with open('usuarios.json' , 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)
    flash('Usuário cadastrado com sucesso!')

    return redirect('/login')



if __name__ == '__main__':
    app.run(debug=True)