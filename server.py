from flask import Flask, render_template, session, flash, redirect, url_for, request
import webbrowser, sqlite3, os
from users import User
from produtos import Produto
from functions import banco_de_dados, lista_de_categorias, enviar_email

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route("/", methods=['GET', 'POST'])
def home():
    db = banco_de_dados()
    itens_novos = db.buscar_itens_novos()
    itens_promo = db.buscar_promos()
    for x in range(len(itens_promo)):
        itens_promo[x][4] = "static/imgprodutos/"+str(itens_promo[x][4])
    for x in range(len(itens_novos)):
        itens_novos[x] = [itens_novos[x][0], itens_novos[x][1], itens_novos[x][2], "static/imgprodutos/"+str(itens_novos[x][3])]
    return render_template('home.html', login=session.get('logado'), admin =session.get('admin'), novos_itens = itens_novos, promo_itens = itens_promo)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    if request.method == "POST":
        dados = [request.form['nome'], request.form['email'], request.form['senha']]
        if dados[0] != "" and dados[1] != "" and dados[2] != "":
            db = banco_de_dados()
            a = [dados[0], dados[1], dados[2], None]
            status = db.cadastrar_usuario(a)
            if status:
                global usuario
                usuario = User(dados[0], dados[1])
                session['logado'] = True
                return redirect(url_for("home"))
            else:
                session['logado'] = False
                flash("Email já cadastrado")
        else:
            flash("Preencha todos os campos")

    return render_template("cadastro.html", login=session.get('logado'), admin =session.get('admin'))


@app.route('/entrar', methods=['GET', 'POST'])
def logar():

    if request.method == "POST":
        email = str(request.form['email'])
        senha = str(request.form['senha'])
        session['admin'] = False
        if email != "" and senha != "":

            if (email == "admin" and senha == "admin"):

                session['admin'] = True
                session['logado'] = True

                return redirect(url_for('home'))
            else:
                db = banco_de_dados()
                status = db.buscar_usuario(email)
                if status:
                    if senha == str(status[1]):
                        global usuario
                        usuario = User(status[0], email)
                        session['logado'] = True
                        return redirect(url_for('home'))
                    else:
                        flash("Senha errada !")
                else:
                    flash("Email não cadastrado !")
        else:
            flash("Preencha todos os campos !")

    return render_template("login.html", login=session.get('logado'), admin =session.get('admin'))


@app.route('/editar', methods=['GET', 'POST'])
def editarCatalogo():

    if session['admin']:
        if request.method == 'GET':
            return render_template("editar_catalogo.html", acao="editarcatalogo",login=session.get('logado'), admin =session.get('admin'))
        elif request.method == 'POST':
            # OPCAO 1 - Add item; OPCAO 2 - Remov item.
            if request.form['opcao'] == "opcao1":
                return redirect(url_for('additem'))
            elif request.form['opcao'] == "opcao2":
                return redirect(url_for('remitem'))
            elif request.form['opcao'] == "addpromo":
                return redirect(url_for('addpromo'))
            elif request.form['opcao'] == "rempromo":
                return redirect(url_for('rempromo'))
            elif request.form['opcao'] == "alteraritem":
                return redirect(url_for("edititem"))

@app.route('/editar/additem', methods=['GET', 'POST'])
def additem():
    if session['admin']:
        if request.method == 'GET':
            return render_template("editar_catalogo.html", acao="opcao1",login=session.get('logado'), admin =session.get('admin'), categs = lista_de_categorias().keys())
        elif request.method == 'POST':
            nome = request.form['nome']
            arq_img = request.form['nome_arq_img']
            preco = request.form['preco']
            categoria = request.form['categoria']
            descricao = request.form['descricao']

            db = banco_de_dados()

            if nome == "" or arq_img == "" or preco == "" or categoria == "":
                flash("Preencha todos os campos !")
            else:
                try:
                    codigo = db.cria_codigo(categoria)
                    db.add_item(codigo, nome, preco, categoria, arq_img, descricao)
                    flash('Item adicionado !')
                except:
                    flash('Algo deu errado !')
            return render_template("editar_catalogo.html",acao="opcao1",login=session.get('logado'), admin =session.get('admin'), categs = lista_de_categorias().keys())


@app.route('/editar/remitem', methods=['GET', 'POST'])
def remitem():
    if session['admin']:
        if request.method == 'GET':
            return render_template('editar_catalogo.html', acao="opcao2",login=session.get('logado'), admin =session.get('admin'))
        elif request.method == 'POST':    
            codigo = request.form['codigo']
            if codigo == "":    
                flash('Preencha o campo !')
            else:
                db = banco_de_dados()
                status = db.del_item(codigo)
                flash(status)
            return render_template('editar_catalogo.html', acao="opcao2",login=session.get('logado'), admin =session.get('admin'))


@app.route('/editar/addpromo', methods=['GET', 'POST'])
def addpromo():
    if session['admin']:
        if request.method == 'GET':
            return render_template("editar_catalogo.html", acao ="addpromo", login=session.get('logado'), admin =session.get('admin'))
        elif request.method == 'POST':
            codigo = request.form['codigo']
            preco_novo = request.form['preco_novo']
            if codigo == "" or preco_novo =="":
                flash("Preencha todos os campos !")
                return render_template("editar_catalogo.html", acao ="addpromo", login=session.get('logado'), admin =session.get('admin'))
            else:    
                db = banco_de_dados()
                status = db.add_promocao(codigo, preco_novo)
                flash(status)
                return render_template("editar_catalogo.html", acao ="addpromo", login=session.get('logado'), admin =session.get('admin'))


@app.route("/editar/rempromo", methods=['GET', 'POST'])
def rempromo():
    if session['admin']:
        if request.method == 'GET':
            return render_template("editar_catalogo.html", acao="rempromo", login=session.get('logado'), admin=session.get('admin'))
        elif request.method == 'POST':
            codigo = request.form['codigo']
            db = banco_de_dados()
            status = db.rem_promocao(codigo)
            flash(str(status))
            return render_template('editar_catalogo.html', acao="rempromo", login=session.get('logado'), admin=session.get('admin'))


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    pass


@app.route('/logout', methods=['GET', 'POST'])
def sair():
    session['logado'] = False
    if session.get('admin'):
        session['admin'] = False
    return redirect(url_for('home'))


@app.route('/categoria', methods=['POST'])
def catalogo():
    db = banco_de_dados()
    categ = request.form['botao-categorias']
    a = db.listar_categoria(categ)
    dic = {'VITAMINAS': "Vitaminas",'WHEYPROTEIN': "Whey Protein",'PROTEINAS': 'Proteínas','OLEOSESSENCIAIS':'Óleos Essenciais','HIPERCALORICOS': 'Hipercalóricos','TERMOGENICOS': 'Termogênicos','PRETREINOS': 'Pré-treinos'}
    categ = dic[categ]
    for x in range(len(a)):
        a[x] = [a[x][0], a[x][1], a[x][2], "static/imgprodutos/"+str(a[x][4])]
    categ = str(categ).capitalize()
    return render_template('catalogo.html', categ=categ, cat=a, login=session.get('logado'), admin =session.get('admin'))


@app.route('/item', methods=['GET', 'POST'])
def pagitem():
    codigo = request.form['codigo']
    db = banco_de_dados()
    infos = db.buscar_item((codigo,))
    # INFOS = [codigo, nome, preco, categoria, img, data, id, descricao]
    infos[4] = "static/imgprodutos/"+str(infos[4])
    return render_template("paginaitem.html", login=session.get('logado'), admin =session.get('admin'), infos = infos)

@app.route('/duvidas', methods=['GET','POST'])
def duvidas():
    if session.get('admin'):
        db = banco_de_dados()
        lista_duvidas = db.listar_duvidas()
        for x in range(len(lista_duvidas)):
            img = db.buscar_item((lista_duvidas[x][0],))
            img = "static/imgprodutos/"+str(img[4])
            lista_duvidas[x] = [lista_duvidas[x][0],lista_duvidas[x][1],lista_duvidas[x][2],lista_duvidas[x][3], img] 
        if 'responder' not in request.form['opcao']:
            return render_template('duvidas.html', login=session.get('logado'), admin =session.get('admin'), duvidas = lista_duvidas, acao="ler")
        else:
            duvida = request.form['opcao'].split(":")
            a = db.buscar_item((duvida[1],))
            duvida.append("static/imgprodutos/"+str(a[4]))
            return render_template('duvidas.html', login=session.get('logado'), admin =session.get('admin'), x = duvida, acao="responder")
            
    else:
        if request.method == "POST":
            if 'enviar' not in request.form['opcao']:
                codigo = request.form['opcao']
                db = banco_de_dados()
                item = db.buscar_item((codigo,))
                item[4] = "static/imgprodutos/"+str(item[4])
                return render_template('duvidas.html', login=session.get('logado'), admin =session.get('admin'), item = item)
            else:
                if session.get('logado'):
                    nome = usuario.mostrar_dados()[0]
                    email = usuario.mostrar_dados()[1]
                else:
                    nome = request.form['nome']
                    email = request.form['email']

                codigo = str(request.form['opcao']).split(":")[1]
                duvida = request.form['duvida']

                if nome == "" or email == "" or duvida == "":
                    flash('Preencha todos os campos')
                    db = banco_de_dados()
                    item = db.buscar_item((codigo,))
                    item[4] = "static/imgprodutos/"+str(item[4])
                    return render_template('duvidas.html', login=session.get('logado'), admin =session.get('admin'), item = item)
                else: 
                    db = banco_de_dados()
                    status = db.enviar_duvida(codigo, nome, email, duvida)
                    if not status:
                        status = "Você já enviou uma dúvida sobre esse produto. Aguarde ela ser respondida para enviar outra"
                    flash(status)
                    item = db.buscar_item((codigo,))
                    item[4] = "static/imgprodutos/"+str(item[4])
                    return render_template('duvidas.html', login=session.get('logado'), admin =session.get('admin'), item = item)
        
@app.route('/duvidas/responder', methods=['POST'])
def responderduvida():
    opcao = request.form['opcao'].split(":")
    nome = opcao[2]
    email = opcao[3]
    codigo = opcao[1]
    resposta = request.form["resposta"]
    db = banco_de_dados()
    item = db.buscar_item((codigo,))
    nome_item = item[1]
    enviar_email(nome, nome_item, email, resposta)
    
    db.deletar_duvida(nome, codigo)
    return redirect(url_for("home"))

webbrowser.open('http:\\localhost:5000', new=1)
app.run(debug=True)
