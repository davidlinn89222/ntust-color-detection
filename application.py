# Import required package
from flask import Flask, render_template, request, url_for, redirect, flash, send_file, jsonify
import os
import json
from lib import main
from lib import detector
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'json'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Build the flask app
app = Flask(__name__)

# setup for the flask app
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(path, 'tmp', 'images')
COLOR_FOLDER = os.path.join(path, 'tmp', 'colors')
DOWNLOAD_FOLDER = os.path.join(path, 'tmp', 'results')

# Make directory if not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.isdir(COLOR_FOLDER):
	os.makedirs(COLOR_FOLDER)

if not os.path.isdir(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# more setup for flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COLOR_FOLDER'] = COLOR_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


# ------------------------------------------------------------------------------------------------------------------

@app.route('/')
def upload_form():
	return render_template("upload.html")


@app.route('/', methods = ["POST"])
def upload_file():

	# delete the images uploaded previously 
	for f in os.listdir(app.config['UPLOAD_FOLDER']):
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

	for f in os.listdir(app.config['COLOR_FOLDER']):
		os.remove(os.path.join(app.config['COLOR_FOLDER'], f))

	if request.method == "POST":
		if 'files1[]' not in request.files:
			return redirect(request.url)
		if 'files2' not in request.files:
			return redirect(request.url)

		imagefiles = request.files.getlist("files1[]")
		colorfile = request.files.get("files2")

		for file in imagefiles:
			if file.filename == '':
				return redirect(redirect.url)

		if colorfile.filename == '':
			return redirect(request.url)

		# process the color definition
		if colorfile and allowed_file(colorfile.filename):
			filename = secure_filename(colorfile.filename)
			colorfile.save(os.path.join(app.config['COLOR_FOLDER'], filename))

		color_spec_dicts = {}
		with open(os.path.join(app.config['COLOR_FOLDER'], colorfile.filename)) as json_file:
			data = json.load(json_file)
			for key, value in data.items():
				color_spec_dicts[key] = []
				for sub_key, sub_value in value.items():
					color_spec_dicts[key].append(sub_value)

		# process the image 
		for file in imagefiles:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		main.main(color_spec_dicts, app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER'])

		return redirect("/download")


@app.route('/download/', methods = ["GET"])
def download_file():
	return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], "out.csv"), as_attachment = True)

if __name__ == "__main__":
	app.run(debug = True)
