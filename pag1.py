from flask import Flask, render_template, session, flash, redirect, url_for, request
import webbrowser, sqlite3, os
from users import User
from produtos import Produto

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template('home.html', login=session.get('logado'), admin = session.get('admin'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if nome is not "" and email is not "" and senha is not"":
            db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
            cursor = db.cursor()
            cursor.execute("""SELECT email FROM usuarios""")
            emailsdb = cursor.fetchall()
            
            if email in emailsdb:
                flash("Email já cadastrado !")
            else:
                global usuario
                usuario = User(nome, email, senha)
                dados = [usuario.nome, usuario.email, usuario.senha]
                cursor.execute("INSERT INTO usuarios VALUES (?,?,?)", dados)
                db.commit()
                session['logado'] = True
                db.close()
                return redirect(url_for("home"))
        else:
            flash("Preencha todos os campos")
    return render_template("cadastro.html")


@app.route('/entrar', methods=['GET', 'POST'])
def logar():
    if request.method == "POST":
        email = str(request.form['email'])
        senha = str(request.form['senha'])
        if email is not "" and senha is not "":
            db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
            cursor = db.cursor()
            cursor.execute("""SELECT senha, nome FROM usuarios WHERE email = '{}'""".format(email))
            senhadb = cursor.fetchall()
            senhadb = senhadb[0]
            nomedb = senhadb[1]

            nomedb = str(nomedb[0])
            senhadb = str(senhadb[0])
            db.close()

            if (email == "admin" and senha == "admin"):
                session['admin'] = True
                session['logado'] = True
                return redirect(url_for('home'))
            if senhadb:
                print(senhadb)
                print(senha)
                if senha in senhadb:
                    global usuario
                    usuario = User(nomedb, email, senha)
                    session['logado'] = True
                    return redirect(url_for('home'))
                else:
                    flash("Senha errada !")
            else:
                flash("Email não cadastrado !")
        else:
            flash("Preencha todos os campos !")
    return render_template("login.html", novos =  [[],[],[]] , promo = ["nome1", "nome2", "nome3"])


@app.route('/editar', methods=['GET', 'POST'])
def editarCatalogo():
    produto = Produto()
    produto.nome = request.form['nome']
    produto.categoria = request.form['categoria']
    produto.preco = request.form['preco']
    cursor.execute( #INSERE DADOS NA TABELA
    """
        INSERT INTO itens (nome,preço,categoria)
        VALUES("{}","{}","{}");
    """.format(produto.nome, produto.preco, produto.categoria)    
    )

    return render_template("editar_catalogo.html")


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    pass


@app.route('/conta', methods=['GET', 'POST'])
def minhaConta():
    pass


webbrowser.open('http:\\localhost:5000', new=1)
app.run(debug=True)