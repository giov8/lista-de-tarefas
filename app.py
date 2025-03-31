# Importando a biblioteca Flask
from flask import Flask, render_template, request, session, redirect, url_for, flash
# Biblioteca para segurança no login
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__) # Criando um objeto do Flask chamado app 

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conexao = database.conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario and usuario[2] == senha:  # Verifica se a senha está correta
            session['usuario'] = usuario[0]  # Armazena o email do usuário na sessão
            return redirect(url_for('home'))
        else:
            flash("Usuário ou senha incorretos!", "danger")
    else:
        return render_template('login.html')

# GET serve para "pegar" as informações de uma página
# POST serve para enviar informações 
@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.criar_usuario(form) == True:
            return render_template('login.html')
        else:
            return "Ocorreu um erro ao cadastrar usuário"
    else:
        return render_template('cadastro.html')

@app.route('/tarefas')
def tarefas():
   return render_template('tarefas.html')


@app.route('/nova', methods=["POST"])
def nova():
    form = request.form
    usuario = session['usuario']
    conteudo = form['conteudo'] 

    if database.criar_tarefa(usuario, conteudo) == True:
        return render_template('login.html')
    else:
        return "Ocorreu um erro ao criar a tarefa"

if __name__ == '__main__':
    app.run(debug=True) 