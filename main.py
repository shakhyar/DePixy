import os
from datetime import timedelta

from PIL import Image

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from config import *
from items import Items


app = Flask(__name__)
app.secret_key = "........"
app.permanent_session_lifetime = timedelta(minutes=10)
items = Items()


@app.route('/')
def index():
	cats = os.listdir(CAT_BASE_DIR)
	print(cats)
	return render_template('index.html', cats=cats)


@app.route('/anime-collection')
def anime_collection():
	return render_template("anime.html", folder="anime")


@app.route('/category/<cat>')
def category(cat):
	THUMBNAIL_PATH = f'categories/{cat}/'

	_items = next(os.walk(CAT_BASE_DIR+'/'+cat+'/'))[1]

	print(items)
	payload = []


	for item in _items:
		i = item[:item.index("=")]
		p = item[item.index("=")+1:]
		thumbnail_path = f"categories/{cat}/{item}/thumbnail.png"
		print(thumbnail_path)
		payload.append((i, p, thumbnail_path))

	return render_template('product-page.html', payload=payload,cat=cat)

@app.route("/product-info/<cat>/<name>")
def product_info(cat, name):
	desc, price, sku, _, = items.read_from_db(name)

	return render_template("product_info.html", p=(name, desc, str(price), sku), cat=cat)


@app.route('/admin-dashboard', methods=['GET', 'POST'])
def dashboard_login():
	if request.method == "POST":
		admin = request.form['email']
		password = request.form['password']
		session.permanent = True
		session['admin'] = admin
		if password == ADMIN_PASSWORD and (admin == ADMIN1 or admin == ADMIN2):
			return redirect(url_for('dashboard'))

		else:
			return render_template('dashboard_login.html', msg = "Invalid Credentials")

	else:
		if 'admin' in session:
			return redirect(url_for('dashboard'))
		else:
			return render_template("dashboard_login.html")

@app.route('/admin-logout')
def a_logout():
	session.pop('admin')
	return redirect(url_for('dashboard_login'))


@app.route('/dashboard')
def dashboard():
	if "admin" in session:
		return render_template('dashboard.html')

	else:
		return redirect(url_for('dashboard_login'))


@app.route('/upload', methods=["GET", "POST"])
def upload():
	if 'admin' in session:
		if request.method == "POST":
			cat = request.form['cat']
			pn = request.form['pn']
			dsc = request.form['dsc']
			price = request.form['price']
			sku = request.form['sku']
			pid = request.form['pid']
			files = request.files.getlist("file")

			###################################TODO########################################
			# add thumbnail compression for faster loading of category/product pages



			##################################TODO:#######################################
			# IMPORTANT
			# STORE THUMBNAILS IN A THUMBNAILS DIRECTORY FOR PROPER EXTRACTION
			
			if os.path.exists(f"{CAT_BASE_DIR}/{cat}/"):
				# for adding more images / update existing
				if os.path.exists(f"{CAT_BASE_DIR}/{cat}/{pn}={price}"):
					print(items.read_all())

					for idx, file in enumerate(files):
						file.save(f"{CAT_BASE_DIR}/{cat}/{pn}={price}/{idx}")

					
				# for creating new product
				else:
					os.mkdir(f"{CAT_BASE_DIR}/{cat}/{pn}={price}")
					items.data_entry(pn, dsc, price, sku, pid)
					print(items.read_all())
					
					for idx, file in enumerate(files):
						print(idx)
						if idx==0:

							file.save(f"{CAT_BASE_DIR}/{cat}/{pn}={price}/{idx}")
							
							img = Image.open((f"{CAT_BASE_DIR}/{cat}/{pn}={price}/{idx}"))
							width, height = img.size
							img = img.resize((width, height), Image.ANTIALIAS)
							img.save(f"{CAT_BASE_DIR}/{cat}/{pn}={price}/thumbnail.png")
						else:
							file.save(f"{CAT_BASE_DIR}/{cat}/{pn}={price}/{idx}")

						
			else:
				# for creating a new category
				print(items.read_all())
				return "category doesnt exist"
				"""os.mkdir(f"{CAT_BASE_DIR}/{cat}/")
				os.mkdir(f"{CAT_BASE_DIR}/{cat}/{pn}={price}")
				for file in files:
					file.save(f"{CAT_BASE_DIR}/{cat}/{pn}={price}/"+secure_filename(file.filename))"""

			return redirect(url_for('upload', msg=f"success for {pn}"))
		else:
			return render_template("add-design.html")
	else:
		return redirect(url_for('dashboard_login'))


@app.route('/add-categories', methods=['GET', 'POST'])
def add_categories():
	if 'admin' in session:
		if request.method == 'POST':
			_cat = request.form['cat']

			if os.path.exists(CAT_BASE_DIR+'/'+_cat):
				return "Category already exists"
			else:
				os.mkdir(CAT_BASE_DIR+'/'+_cat)
				f = request.files['file']
				f.save(f"{CAT_BASE_DIR}/{_cat}/category-img")
				return redirect(url_for('add_categories'))
		else:
			return render_template('add_categories.html')
	else:
		return redirect(url_for('dashboard_login'))
		

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		_email = request.form['email']
		_pass = request.form['password']
		pass

	else:
		if None:
			pass


@app.route('/tnc')
def tnc():
	return render_template('tnc.html')
@app.route('/privacy')
def pp():
	return render_template('pp.html')

@app.route('/returnpolicy')
def rp():
	return render_template('rp.html')

@app.route('/about-us')
def abs():
	return render_template('aboutus.html')

@app.route('/contact-us')
def cs():
	return render_template('contact.html')


@app.route('/revenue', methods=['GET', 'POST'])
def revenue():
	if 'admin' in session:
		return render_template('revenue.html')
	else:
		return 


if __name__ == '__main__':
	app.run(debug=True)