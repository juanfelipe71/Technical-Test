from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/technical_test'
db = SQLAlchemy(app)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'technical_test'
mysql = MySQL(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    mac_address = db.Column(db.String(17))
    serial_number = db.Column(db.String(50))
    manufacturer = db.Column(db.String(100))
    description = db.Column(db.Text)

@app.cli.command()
def create_db():
    db.create_all()

@app.route('/inventory')
def list_inventory():
    data = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT id, name, price, mac_address, serial_number, manufacturer, description FROM inventory"
        cursor.execute(sql)
        inventory = cursor.fetchall()
        data['inventory'] = inventory
        data['mensaje'] = 'exito'
    except Exception as ex:
        data['mensaje'] = 'error...'
    finally:
        cursor.close()
    return jsonify(data)

@app.route('/')
def index():
    inventory_items = Inventory.query.all()
    return render_template('index.html', inventory=inventory_items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        mac_address = request.form['mac_address']
        serial_number = request.form['serial_number']
        manufacturer = request.form['manufacturer']
        description = request.form['description']
        
        new_item = Inventory(name=name, price=price, mac_address=mac_address, serial_number=serial_number, manufacturer=manufacturer, description=description)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Inventory.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.mac_address = request.form['mac_address']
        item.serial_number = request.form['serial_number']
        item.manufacturer = request.form['manufacturer']
        item.description = request.form['description']
        
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)