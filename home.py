from flask import Flask, render_template, request, redirect
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

# class agendamentos:
#     def __init__(self, nome, categoria, data, hora):
#         self.nome = nome
#         self.categoria = categoria
#         self.data = data
#         self.hora = hora

# agendamento1 = agendamentos('João', 'Consulta', '2023-10-01', '10:00')
# agendamento2 = agendamentos('Maria', 'Exame', '2023-10-02', '11:00')
# lista = [agendamento1, agendamento2]   


def get_agendamentos():
    cursor.execute('SELECT * FROM agendamentos')
    return cursor.fetchall()


@app.route('/agendamentos')
def teste():
    agendamentos = get_agendamentos()
    return render_template('agendamentos.html', agendamentos=agendamentos)



@app.route('/novo', methods=['GET', 'POST'])
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
    return redirect('/agendamentos')

if __name__ == '__main__':
    app.run(debug=True)