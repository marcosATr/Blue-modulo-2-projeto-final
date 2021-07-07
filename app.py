from flask import Flask, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user='nyytdlog'
password='n5P951qOmJv2a0L1Z7n3BtNyiugRGcsQ'
host='tuffi.db.elephantsql.com'
database='nyytdlog'


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db = SQLAlchemy(app)


class Receitas(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nome = db.Column(db.String(50), nullable = False)
  imagem_url = db.Column(db.String(255), nullable = False)
  video_url = db.Column(db.String(255), nullable = True)
  ingredientes = db.Column(db.Text, nullable = True)
  tipo = db.Column(db.String(50), nullable = False)


  def __init__(self, nome, imagem_url, video_url, ingredientes, tipo):
    self.nome = nome
    self.imagem_url = imagem_url
    self.video_url = video_url
    self.ingredientes = ingredientes
    self.tipo = tipo

  @staticmethod
  def todas_receitas():
    return Receitas.query.order_by(Receitas.id.desc()).all()
    #return Receitas.query.all()

  @staticmethod
  def exibir_detalhe(id):    
    return Receitas.query.get(id)

  @staticmethod
  def por_categoria(tipo):
    return Receitas.query.filter_by(tipo=tipo).order_by(Receitas.id.desc()).all()
  
  def salvar(self): 
    db.session.add(self) 
    db.session.commit()

  def update(self, new_data):
    self.nome = new_data.nome
    self.imagem_url = new_data.imagem_url
    self.video_url = new_data.video_url
    self.ingredientes = new_data.ingredientes
    self.tipo = new_data.tipo
    self.salvar()

  def delete(self):
    db.session.delete(self) 
    db.session.commit()
  

#ROTAS DA HOMEPAGE LISTAM TODAS AS RECEITAS
@bp.route('/')
@bp.route('/index')
@bp.route('/home')
def home():
  receitas = Receitas.todas_receitas()
  return render_template('index.html', receitas=receitas) 

@bp.route('/<id>')
def exibir_detalhe(id):
  receita = Receitas.exibir_detalhe(id)

  return render_template('exibir_detalhe.html', receita=receita)

##LISTAR POR TIPO

@bp.route('/categoria/<tipo>')
def por_categoria(tipo):
  receitas = Receitas.por_categoria(tipo)
  return render_template('por_categoria.html', receitas=receitas)



@bp.route('/cadastrar', methods=('GET', 'POST'))
def cadastrar():

  id_atribuido = None

  if request.method =='POST':
    form=request.form
    receitas = Receitas(form['nome'],form['imagem_url'],form['video_url'], form['ingredientes'], form['tipo']) 
    receitas.salvar()
    id_atribuido=receitas.id
  return render_template('cadastrar.html', id_atribuido=id_atribuido)


@bp.route('/update/<id>',methods=('GET', 'POST'))
def update(id):
  sucesso = None
  receita = Receitas.exibir_detalhe(id)  

  if request.method =='POST':
    form=request.form

    new_data= Receitas(form['nome'],form['imagem_url'], form['video_url'], form['ingredientes'], form['tipo']) 

    receita.update(new_data)

    sucesso = True

  return render_template('update.html', receita=receita,sucesso=sucesso)


@bp.route('/delete/<id>') 
def delete(id):
  receita = Receitas.exibir_detalhe(id)

  return render_template('delete.html', receita=receita)


@bp.route('/delete/<id>/confirmed') 
def delete_confirmed(id):

  sucesso = None
  receita = Receitas.exibir_detalhe(id)

  if receita:
    receita.delete()
    sucesso = True

  return render_template('delete.html', sucesso=sucesso)

app.register_blueprint(bp)


if __name__ == '__main__':
  app.run(debug=True)