from flask import Flask, render_template, redirect, request, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'INACIO'
class agendamentos:
    def __init__(self, nome, categoria, data, hora):
        self.nome = nome
        self.categoria = categoria
        self.data = data
        self.hora = hora

@app.route('/teste')
def teste():
    agendamento1 = agendamentos('João', 'Consulta', '2023-10-01', '10:00')
    agendamento2 = agendamentos('Maria', 'Exame', '2023-10-02', '11:00')
    lista = [agendamento1, agendamento2]   
    return render_template('teste.html', agendamentos=lista)

if __name__ == '__main__':
    app.run(debug=True)
