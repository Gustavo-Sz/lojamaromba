from flask import Flask, render_template, session, flash, redirect, url_for, request
import webbrowser, sqlite3, os
from classes import user

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html', login=session.get('logado'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
        cursor = db.cursor()
        cursor.execute("""SELECT email FROM usuarios""")
        emailsdb = cursor.fetchall()
        db.close()

        if email in emailsdb:
            sucess = False
            flash("Email já cadastrado !")
        else:
            global usuario
            usuario = user(nome, email, senha)
            session['logado'] = True
            return redirect(url_for("home"))
    return render_template("cadastro.html")


@app.route('/entrar', methods=['GET', 'POST'])
def logar():

    if request.method == "POST":

        email = request.form['email']
        senha = request.form['senha']

        db = sqlite3.connect(r"{}\db.db".format(os.getcwd()))
        cursor = db.cursor()
        cursor.execute("""SELECT senha FROM usuarios WHERE email = '{}'""".format(email))
        senhadb = cursor.fetchall()
        db.close()

        if senhadb:
            if senha in senhadb:
                global usuario
                usuario = user(nome, email, senha)
                session['logado'] = True
                return redirect(url_for('home'))
            else:
                flash("Senha errada !")
        else:
            flash("Email não cadastrado !")
    return render_template("logar.html")

@app.route('/editar', methods=['GET', 'POST'])
def editar_catalogo():
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



webbrowser.open('http:\\localhost:5000', new=1)
app.run(debug=True)
