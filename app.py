from flask import Flask, redirect, url_for, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
import models
from json import load

app = Flask(__name__)
with open('db_config.json') as file:
    data = load(file)
    app.secret_key = data['secret_key']
    app.config['SQLALCHEMY_DATABASE_URI'] = data['uri']
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user, senha):
    return models.User.query.filter_by(usuario=user, senha=senha)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        user = request.form['usuario']
        senha = request.form['senha']
        usuario = models.Usuario.query.filter_by(usuario=user, senha=senha).first()
        if usuario:
            login_user(usuario)
            return redirect(url_for('estoque', usuario=usuario.usuario))
        else:
            return render_template('login.html', erro='Usuario não cadastrado')
        
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('sign.html')
    if request.method == 'POST':
        user = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']
        status = 'admin'
        db.session.add(models.Usuario(user, email, senha, status))
        db.session.commit()
        return redirect(url_for('estoque'))

@app.route('/estoque')
@login_required
def estoque():
    return render_template('estoque.html', produtos=models.Produto.query.all(), usuario='usuario')

@app.route('/estoque/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method == 'GET':
        return render_template('produto.html')
    
    elif request.method == 'POST':
        id = request.form['codigo']
        nome = request.form['nome']
        categoria = request.form['categoria']
        medida = request.form['medida']
        custo = request.form['custo']
        valor = request.form['valor']
        db.session.add(models.Produto(id, nome, categoria, medida, custo, valor))
        db.session.commit()
        return redirect(url_for('estoque', produtos=models.Produto.query.all(), usuario=session['user'][0]))

@app.route('/estoque/edit/<id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    if request.method == 'GET':
        produto = models.Produto.query.filter_by(id=id).first()
        print(produto)
        return render_template('produto.html')


if __name__ == '__main__':
    db.create_all()
    
    app.run(debug=True)