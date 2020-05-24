# if time, redo the account stuff
import os
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob

from flask import Flask, flash, jsonify, redirect, render_template, request, session, current_app, app, send_from_directory
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Upload folder place
UPLOAD_FOLDER = '/home/ubuntu/project/implementation/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# typically, i use area = 3.81E-7 and L0 = 0.01 for the area and L0 settings
lin_regime = 5
domain = 600 # resolution of file

# to use for .png names; generate a random sequence of letters to avoid overlap
def randid():
    return ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(8))

# file extraction
def Extract(filename):
    time = []
    ext = []
    load = []
    csvfile = open(filename,'r')
    lines = csvfile.readlines()
    for line in lines:
        try:
            line = line.strip('\r\n').split('"')
            time.append(float(line[1]))
            ext.append(float(line[3])/1000.) # in meters
            load.append(float(line[5]))
        except:
            continue

    return time, ext, load

# plotting file
def Plot_Process(filename, area, L0, color):
    time, ext, load = Extract(filename)

    # make time, ext, load into np arrays
    time = np.asarray(time)
    ext = np.asarray(ext)
    load = np.asarray(load)

    # converting units and force -> stress, extension -> strain
    stress = load/(area*10**6)
    stress = stress - stress[0]
    strain = ext/L0
    strain = strain - strain[0]

    # plot the graph
    plt.plot(strain, stress, linewidth=4, color=color, alpha=0.1)
    plt.xlabel('Strain', fontsize=20)
    plt.ylabel('Stress (MPa)', fontsize=20)
    plt.ylim((0,30))
    plt.xlim((0,5))
    plt.tick_params(labelsize=20, width=2, length=7)
    return strain[0:domain], stress[0:domain]

# downloading file
@app.route('/uploads/<path:filename>')
def download(filename):
    # make path to uploads absolute
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])  # https://stackoverflow.com/questions/24577349/flask-download-a-file
    return send_from_directory(uploads, filename, as_attachment = True)

@app.route("/", methods=["GET", "POST"])
def info():
    """homepage"""

    return render_template("info.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    """File uploading and data analysis"""

    # clean out any previous plots
    plt.clf()

    if request.method == 'POST':
        if 'file' not in request.files:
            return apology('No file part', 403)

        files = request.files.getlist('file')
        # if user does not select file, browser also
        # submit an empty part without filename
        if request.files['file'].filename == '':
            return apology('Must provide files', 403)

        # generate a random name for the file and save it to the uploads folder
        filelist = []
        for file in files:
            if file and file.filename:
                filename = randid() + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filelist.append(filename)

        try:
            area = float(request.form.get("area"))
            L0 = float(request.form.get("L0"))
        except ValueError:
            apology("Please provide a valid value!", 403)

        # navigate to the uploads folder
        os.chdir('uploads')
        # making arrays for stress, E (Young's modulus), and strain
        stress_list = []
        E = []
        strain = []
        for csv in filelist:
            strain, stress = Plot_Process(csv, area, L0, 'k')
            params = np.polyfit(strain[0:lin_regime], stress[0:lin_regime], 1) # polynomial fit of degree 1 to first six points in strain and stress (we just want to see the initial linear increase, and this is enough)
            E.append(params[0]) # add to the array of Young's moduli
            stress_list.append(stress) # add to array of stress

        # plot the average curve in black
        stress_avg = sum(stress_list)/len(stress_list)
        x = np.array(strain)
        y = np.array(stress_avg)
        plt.plot(x, y, linewidth=4, color='k')
        params = np.polyfit(x, stress_avg, 1)

        # plot the initial linear increase in red -- the slope is Young's modulus
        E = np.array(E)
        strain = np.array(strain)
        plt.plot(strain, strain*np.mean(E), color='r')
        plt.tight_layout()

        # give image a name
        image_name = randid() + '.png'

        # save the image and navigate out of the folder (so next iteration you can navigate in again)
        plt.savefig(image_name)
        os.chdir('..')

        return render_template("results.html", url = '/uploads/' + image_name, modulus = np.mean(E), std = np.std(E))

    if request.method == "GET":
        # return template
        return render_template("index.html")

def apology(message, code=400):  # thank you to CS50
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def errorhandler(e):  # thanks, CS50!
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors. Thanks, CS50!!!
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)