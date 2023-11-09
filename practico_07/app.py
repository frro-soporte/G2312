from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from models import Socio
from Database import Database
from DataSocio import DataSocio
from forms import SocioForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Database.configura_conexion()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'registro_socios'
Database.db.init_app(app)
migrate = Migrate()
migrate.init_app(app, Database.db)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def get_all_socios():
    socios = DataSocio.get_all_socios()
    return render_template('index.html', sociosParam = socios)

@app.route('/edicion/<int:id>', methods=['GET', 'POST'])
def edit(id):
    socio = Socio.query.get_or_404(id)
    socio_form = SocioForm(obj = socio)

    if request.method == 'POST':
        if socio_form.validate_on_submit():
            socio_form.populate_obj(socio)
            Database.db.session.commit()
            return redirect(url_for('get_all_socios'))

    return render_template('editar.html', socio_editar = socio_form)

@app.route('/agregar', methods=['GET', 'POST'])
def add_socio():
    socio = Socio()
    socio_form = SocioForm(obj = socio)
    if request.method == 'POST':
        #Pregunto si el formulario es válido
        if socio_form.validate_on_submit():
            # Recupero los valores del formulario y los paso al objeto 'socio'
            socio_form.populate_obj(socio)
            DataSocio.add_socio(socio)
        #Me redirecciono a la página principal
        return redirect(url_for('get_all_socios'))
    return render_template('agregar.html', socio_agregar = socio_form)

@app.route('/eliminar/<int:id>')
def delete(id):
    socio = Socio.query.get_or_404(id)
    Database.db.session.delete(socio)
    Database.db.session.commit()
    return redirect(url_for('get_all_socios'))