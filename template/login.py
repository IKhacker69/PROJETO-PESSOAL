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
                else:
                    flash('Usuário ou senha incorretos!')
                    return redirect('/login')
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)