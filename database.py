import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key,nome text,senha text)''')
    
    cursor.execute('''create table if not exists tarefas
                   (id integer primary key, conteudo text, esta_concluida integer, email_usuario text,
                   FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    
    conexao.commit()

def criar_usuario (formulario):
    # Ver se já existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()

    quantidade_de_emails_cadastrados = cursor.fetchone()
    print(quantidade_de_emails_cadastrados)
    if (quantidade_de_emails_cadastrados[0] > 0):
        print("LOG: Já existe esse e-mail cadastrado no banco!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute(''' INSERT INTO usuarios (email, nome, senha)
                   VALUES (?, ?, ?)''', 
                   (formulario['email'], formulario['nome'], senha_criptografada))
    conexao.commit()
    return True

def fazer_login (formulario):
    # Ver se já existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()

    quantidade_de_emails_cadastrados = cursor.fetchone()
    print(quantidade_de_emails_cadastrados)
    if (quantidade_de_emails_cadastrados[0] < 0):
        print("LOG: Não existe esse e-mail cadastrado no banco!")
        return False
    else:
        cursor = conexao.cursor()
        cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
        conexao.commit()
        senha_criptografada = cursor.fetchone()
        resultado_verificacao = check_password_hash(senha_criptografada[0], formulario['senha'])
        return resultado_verificacao

def criar_tarefa(conteudo, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' INSERT INTO tarefas (conteudo, esta_concluida, email_usuario)
                   VALUES (?, ?, ?)''', 
                   (conteudo, False, email))
    conexao.commit()
    return True

def buscar_tarefas(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id, conteudo, esta_concluida
                   FROM tarefas WHERE email_usuario=?''', 
                   (email,))
    conexao.commit()
    tarefas = cursor.fetchall() # Busca todos os resultados do select e guarda em "tarefas"
    return tarefas

def marcar_tarefa_como_feita(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    # Vai buscar no banco para ver se a tarefa está concluida ou não
    cursor.execute('''SELECT esta_concluida FROM tarefas WHERE id=?''', (id,))
    esta_concluida = cursor.fetchone()
    esta_concluida = esta_concluida[0]
    print(esta_concluida)
    
    if (esta_concluida):
        esta_concluida = False
    else:
        esta_concluida = True

    cursor.execute('''UPDATE tarefas set esta_concluida = ? where id = ?''', (esta_concluida, id))
    conexao.commit()
    return True

def excluir_tarefa(id, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Verificar se o email que quer excluir a tarefa é realmente dono da tarefa
    cursor.execute('''SELECT email_usuario FROM tarefas WHERE id=?''', (id,))
    conexao.commit()
    email = cursor.fetchone()
    print(email[0])
    print("email enviado: ", email)
    if (email[0] != email[0]):
        return False
    else:
        cursor.execute('''DELETE FROM tarefas WHERE id=?''', (id,))
        conexao.commit()
        return True

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM tarefas WHERE email_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True

if __name__ == '__main__':
    criar_tabelas()