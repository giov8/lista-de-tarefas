from flask import Flask, render_template, request, session, redirect, url_for
import database

app = Flask(__name__) # Criando um objeto do Flask chamado "app"
app.secret_key = "SENHA SECRETA" # Senha secreta que geralmente estaria em um arquivo a parte

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if database.fazer_login(form) == True:
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('lista'))
        else:
            return "Ocorreu um erro ao fazer login"
    else:
        return render_template('login.html')

@app.route('/lista')
def lista():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    lista_tarefas = database.buscar_tarefas(session['usuario'])
    print(lista_tarefas)

    return render_template('lista.html', tarefas=lista_tarefas)    

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

@app.route('/criar_tarefa', methods=["POST"])
def criar_tarefa():
    form = request.form
    
    if database.criar_tarefa(form['conteudo'], session['usuario']) == True:
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao cadastrar a tarefa"

@app.route('/tarefas/atualizar/<int:id>', methods=["GET"])
def marcar_tarefa_como_feita(id):

    if database.marcar_tarefa_como_feita(id):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao marcar a tarefa como feita"


@app.route('/tarefas/excluir/<int:id>', methods=["GET"])
def excluir_tarefa(id):

    email = session['usuario'] # pega o e-mail da sessão para verificar se é o dono da tarefa

    if database.excluir_tarefa(id, email):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao excluir a tarefa"

@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']

    if database.excluir_usuario(email):
        return redirect(url_for('hello'))
    else:
        return "Ocorreu um erro ao excluir o usuário"

if __name__ == '__main__':
    app.run(debug=True) 