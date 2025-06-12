from flask import Flask, render_template, redirect, request, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'INACIO'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods =['POST'])
def login():
    
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    if nome == 'admin' and senha == '1234':
        return render_template('login.html')
    else:
        flash('Usuário ou senha inválidos', 'error')
        return redirect('/')
    
if __name__ in '__main__':
    app.run(debug=True)