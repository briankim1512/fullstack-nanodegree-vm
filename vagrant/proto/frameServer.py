from flask import Flask, render_template, abort, url_for, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__, template_folder='pageDir')

@app.route('/restaurant/<int:restaurant_id>/')
def restMenu(restaurant_id):

	listRestaurant = session.query(Restaurant.name, Restaurant.id\
	).filter(Restaurant.id==restaurant_id).first()
	
	listMenu = session.query(MenuItem.name, MenuItem.price, \
	MenuItem.description, MenuItem.id).filter(MenuItem.restaurant_id==\
	listRestaurant[1])

	return render_template('menu.html', restaurantName=listRestaurant[0], \
	restaurantId=listRestaurant[1], listMenu=listMenu)

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = \
			restaurant_id, course = request.form['course'], description = \
			request.form['description'], price = request.form['price'])
		session.add(newItem)
		session.commit()
		flash('New Item Menu Created')
		return redirect(url_for('restMenu', restaurant_id = restaurant_id))
	if request.method == 'GET':
		return render_template('newMenu.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/<string:modifier>/',\
	methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id, modifier):
	if request.method == 'POST':
		if modifier == "edit":
			editItem = session.query(MenuItem).filter(MenuItem.id==menu_id).\
				first()
			editItem.name = request.form['name']
			editItem.restaurant_id = restaurant_id
			editItem.course = request.form['course']
			editItem.description = request.form['description']
			editItem.price = request.form['price']
			session.commit()
			flash('Menu Item Modified')
			return redirect(url_for('restMenu', restaurant_id = restaurant_id))
		elif modifier == "delete":
			delMenu = session.query(MenuItem).filter(MenuItem.id==menu_id).\
				first()
			session.delete(delMenu)
			session.commit()
			flash('Menu Item Deleted')
			return redirect(url_for('restMenu', restaurant_id = restaurant_id))
		else:
			abort(404)
	if request.method == 'GET':
		if modifier == "edit":
			output = render_template('editMenu.html', restaurant_id=\
				restaurant_id, menu_id=menu_id)
		elif modifier == "delete":
			output = render_template('deleteMenu.html', restaurant_id=\
				restaurant_id, menu_id=menu_id)
		else:
			abort(404)
		return output

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
