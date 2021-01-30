# Import required package
from flask import Flask, render_template, request, url_for, redirect, flash, send_file
import os 
from lib import main
from lib import detector

# Build the flask app
app = Flask(__name__)

# setup for the flask app
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
global path
path = os.getcwd()

# file Upload
UPLOAD_FOLDER = os.path.join(path, 'images')
DOWNLOAD_FOLDER = os.path.join(path, 'results')

# Make directory if not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if not os.path.isdir(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)


# more setup for flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

	if request.method == "POST":
		if 'files[]' not in request.files:
			return redirect(request.url)

		imagefiles = request.files.getlist("files[]")

		for file in imagefiles:
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

		main.main(app.config['UPLOAD_FOLDER'], app.config['DOWNLOAD_FOLDER'])
		return redirect("/download")

@app.route('/download/', methods = ["GET"])
def download_file():
	return send_file("out.csv", as_attachment = True)

if __name__ == "__main__":
	app.run(debug = True)