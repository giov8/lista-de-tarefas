### 🛠 **Projeto Lista de Tarefas**  

**Tecnologias:**  
- Python  
- Flask  
- HTML + CSS  

---

### ✅ **Requisitos do sistema**  

1. **Ver Página Inicial**  
   - Mostrar opções: Login | Criar Conta.  
   
2. **Criar uma conta**  
   - Formulário: Nome, E-mail, Senha.  
   - Salvar no banco de dados (`usuarios`).  

3. **Fazer login no sistema**  
   - Formulário: E-mail, Senha.  
   - Verificar se o usuário existe e se a senha bate.  
   - Se sim, salvar o login na sessão (`session` do Flask).  

4. **Criar, editar e excluir tarefas**  
   - Tela principal após login.  
   - CRUD de tarefas associadas ao usuário logado.  
   - Usar o e-mail do usuário para relacionar tarefas.  

5. **Marcar tarefa como feita**  
   - Atualizar o campo `esta_concluida` no banco.  

6. **Excluir a conta**  
   - Deletar o usuário da tabela `usuarios`.  
   - Deletar todas as tarefas dele da tabela `tarefas`.  

---

### 🖼 **Protótipo (4 Telas)**  

1. Página Inicial  
2. Login  
3. Cadastro  
4. Página de Tarefas  

---

### 🗃 **Diagrama Banco de Dados**  
**Tabelas:**  
- `usuarios`  
  - email (primary key)  
  - nome  
  - senha  

- `tarefas`  
  - id (primary key)  
  - conteudo  
  - esta_concluida (0 ou 1)  
  - email_usuario (foreign key)
