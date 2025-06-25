from flask import Flask, render_template, request, redirect, url_for
import pymysql

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='usuarios'

    )

app = Flask(__name__)
app.config['SECRET_KEY'] = 'INACIO'

cursor = conexao.cursor(pymysql.cursors.DictCursor)


def get_agendamentos():
    cursor.execute('SELECT * FROM agendamentos')
    return cursor.fetchall()


@app.route('/agendamentos')
def teste():
    agendamentos = get_agendamentos()
    return render_template('agendamentos.html', agendamentos=agendamentos)



@app.route('/novo', methods=['get','POST'])
def novo():
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

if __name__ == '__main__':
    app.run(debug=True)