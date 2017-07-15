from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/"):
				self.send_response(301)
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				tempq = ""
				output += "<html><body>"
				output += "<a href='/restaurant/new'><h1>Make a new restaurant</h1></a>"
				for name in session.query(Restaurant.name):
					for idtemp in session.query(Restaurant.id).filter(Restaurant.name==name[0]):
						idnum=idtemp[0]
					output += str(name[0])+"<br>"\
					+"<a href='/restaurant/"+str(idnum)+"/editRN'>Edit</a><br>"\
					+"<a href='/restaurant/"+str(idnum)+"/deleteRN'>Delete</a><br>"	
				self.wfile.write(output)
				print output
				return
			
			if self.path.endswith("/restaurant/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				tempq = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>\
				           <h2>What is the new restaurant name?</h2><input name='message' type='text'>\
						   <input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/editRN"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				pathid = str(self.path)[12:str(self.path).find("/editRN")]
				print pathid

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/"+str(pathid)+"/editRN'>\
				           <h2>What is the new restaurant name?</h2><input name='message' type='text'>\
						   <input type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/deleteRN"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				pathid = str(self.path)[12:str(self.path).find("/deleteRN")]
				print pathid

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/"+str(pathid)+"/deleteRN'>\
				           <h2>Are you sure you want to delete this restaurant entry?</h2>\
						   <input type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output)
				print output
				return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurant/new"):
				self.send_response(301)

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')
			
				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_header("Location", "/restaurant")
				self.end_headers()
			
			if self.path.endswith("/editRN"):
				self.send_response(301)

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				pathid = str(self.path)[12:str(self.path).find("/editRN")]

				editRestaurant = session.query(Restaurant).filter(Restaurant.id==int(pathid)).first()
				session.add(editRestaurant)
				editRestaurant.name = messagecontent[0]
				session.commit()

				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/deleteRN"):
				self.send_response(301)

				pathid = str(self.path)[12:str(self.path).find("/deleteRN")]

				editRestaurant = session.query(Restaurant).filter(Restaurant.id==int(pathid)).first()
				session.delete(editRestaurant)
				session.commit()

				self.send_header('Location', '/restaurant')
				self.end_headers()

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print " has been called. Stopping server"
		server.socket.close()

if __name__ == '__main__':
	main()
