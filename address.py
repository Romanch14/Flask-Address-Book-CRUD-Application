from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate

#Create a Flask application object and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///address_book.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#define the database model
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50), unique = True, nullable = False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(120))

    def __repr__(self):
        return f'<Contact {self.name}>'

# the routes for the application. You can create a form to add new contacts and a table to display existing contacts
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        contact = Contact(name=name, email=email, phone=phone, address = address)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_contact.html')

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        contact.address = request.form['address']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete.<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_contact', methods=['POST'])
def update_contact():
    contact_id = request.form['id']
    contact = Contact.query.get_or_404(contact_id)

    contact.name = request.form['name']
    contact.email = request.form['email']
    contact.phone = request.form['phone']
    contact.address = request.form['address']

    db.session.commit()
    return redirect(url_for('index'))

#for run this code in terminal steps
#step1==  $env:FLASK_APP = "address.py"
#step2== flask run --debug