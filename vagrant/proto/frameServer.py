from flask import Flask, render_template, abort
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

@app.route('/restaurant/<int:restaurant_id>/new/')
def newRestMenu(restaurant_id):
	return render_template('newMenu.html')

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/<string:modifier>/')
def editRestMenu(restaurant_id, menu_id, modifier):
	if modifier == "edit":
		output = render_template('editMenu.html')
	elif modifier == "delete":
		output = render_template('deleteMenu.html')
	else:
		abort(404)
	return output

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
    