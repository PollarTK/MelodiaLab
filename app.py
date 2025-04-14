from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = "chave_muito_segura"
import database

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"]) #rota para a página de login
def login():
    if request.method == "POST":
        form = request.form
        if database.fazer_login(form) == True:
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    lista_musicas = database.buscar_musicas(session['usuario'])

    return render_template('home.html', musicas=lista_musicas)

@app.route('/cadastro', methods=["GET","POST"]) #rota para a página de login
def cadastro():
    if request.method == "POST":
        form = request.form

        if database.criar_usuario(form) == True:
            return render_template('login.html')
        
        else:
            return "Ocorreu um erro ao cadastrar o Usuário"

    else:
        return render_template('cadastro.html')
    
@app.route('/criar_musica', methods=["GET","POST"]) #rota para a pagina de criação
def criar_musica():
    if request.method == "POST":
        form = request.form

        if database.criar_musica(form['titulo'],form['autor'],form['conteudo'],form['status'], session['usuario']) == True:
            return redirect(url_for('home'))
        
        else:
            pass

    else:
        return render_template('criar_musica.html')
    
@app.route('/musicas/editar/<int:id>', methods=["GET", "POST"])
def editar_musica(id):
    # pega o e-mail da sessão para verificar se é o dono da tarefa
    email = session['usuario']
    if (request.method == "GET"):
        conteudo_musica = database.buscar_conteudo_musica(id)
        return render_template('editar.html', musica=conteudo_musica, id=id)
    if (request.method == "POST"):
        form = request.form
        novo_titulo = form['titulo']
        novo_autor = form['autor']
        novo_status = form['status']
        novo_conteudo = form['conteudo']
        database.editar_musica(novo_titulo,novo_autor,novo_status,novo_conteudo, id)
        return redirect(url_for('home'))
    
@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']

    if database.excluir_usuario(email):
        return redirect(url_for('cadastro'))
    else:
        return "Ocorreu um erro ao excluir o usuário"
    
@app.route('/musicas/excluir/<int:id>', methods=["GET"])
def excluir_musica(id):

    email = session['usuario']

    if database.excluir_musica(id, email):
        return redirect(url_for('home'))
    else:
        return "Ocorreu um erro ao excluir a Música!"


# parte principal do
if __name__ == '__main__':
    app.run(debug=True)