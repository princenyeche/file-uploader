#!/usr/bin/env python
"""
Script   : Image Upload Service
Author   : Prince Nyeche
Platform : Web
Version  : 0.1
Function : Script helps to upload single image or multiple images file in a
           zip folder to a Server
**************************************************************************
Required libraries : Flask
Download URL       : pip install -r requirements.txt
License            : MIT License Copyright (c) 2020 Prince Nyeche
**************************************************************************
"""
from flask import (
    Flask, flash, redirect, render_template, request, url_for,
    send_from_directory)
from werkzeug.utils import secure_filename
import os
import random
import string
from shutil import unpack_archive


basedir = os.path.abspath(os.path.dirname(__file__))
rand = os.urandom(16)
app = Flask(__name__)
UPLOAD_FOLDER = "Images/files"
app.config.from_mapping(
    SECRET_KEY=f'{rand}',
)
app.config["UPLOAD_FOLDER"] = os.path.join(basedir, UPLOAD_FOLDER)
ACCEPTED_EXT = {"png", "jpg", "jpeg", "gif", "zip"}
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
our_dir = os.path.join(app.config["UPLOAD_FOLDER"])

if not os.path.exists(our_dir):
    os.makedirs(our_dir)


# here we generated a random string for our folder below
def stringer(n: int = 15):
    chars = string.ascii_letters
    return "".join(random.choice(chars) for j in range(n))


x = stringer(19)
folder = os.path.join(our_dir, x)

# a simple page that says hello
@app.route("/hello")
def hello():
    return "Hello, World!"


# allows us to determine the file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ACCEPTED_EXT


# Our GUI begins
@app.route("/")
def index():
    return render_template("upload/index.html")


# main file processing service
@app.route("/uploader", methods=("GET", "POST"))
def uploader():
    multiple_files = []
    filename = None
    success = None
    error = None
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            error = "File has not been Selected"
            flash(error)
        elif file and allowed_file(file.filename):
            if ".zip" in file.filename:
                list_file = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], list_file))
                save = os.path.join(app.config["UPLOAD_FOLDER"], list_file)
                # extract all files and iterate through it.
                unpack_archive(save, folder)
                # if the zip is in this dir, delete it
                if os.path.isfile(save):
                    os.remove(save)
                if os.path.isdir(folder):
                    for name in os.listdir(folder):
                        # get a direct path to the secured file dir
                        z = os.path.join(folder, name)
                        # on macOs the file and other dir are auto
                        # create, we want to delete that as well
                        if ".zip" in z:
                            os.remove(z)
                        elif ".DS_Store" in z:
                            os.remove(z)
                        elif "__" in z:
                            os.rmdir(z)
                        else:
                            for name in os.listdir(z):
                                multiple_files.append(name)

            else:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            error = "File type not supported, only Images allowed."
            flash(error)
    return render_template('upload/uploading.html',  data=multiple_files, filename=filename, \
                       error=error, success=success)


# allows you to view multiple images or single images
@app.route("/view/<path:filename>", methods=("GET", "POST"))
def view(filename):
    if os.path.exists(folder):
        for file in os.listdir(folder):
            k = os.path.join(folder, file)
            if os.path.isdir(k):
                for m in os.listdir(k):
                    return send_from_directory(k, m)
    else:
        return send_from_directory(our_dir, filename)


# allows you to delete multiple image or single images
@app.route("/delete/<path:filename>", methods=("GET", "POST"))
def delete(filename):
    if os.path.exists(folder):
        for f in os.listdir(folder):
            k = os.path.join(folder, f)
            if os.path.isdir(k):
                for m in os.listdir(k):
                    s = os.path.join(k, m)
                    os.remove(s)
                os.rmdir(k)
            os.rmdir(folder)
        return redirect(url_for("index"))
    else:
        z = os.path.join(our_dir, filename)
        os.remove(z)
        return redirect(url_for("index"))


# create an API version of the endpoint above.
# to access the resource via API, e.g curl
@app.route("/api", methods=("GET", "POST"))
def api():
    multiple_files = []
    show = []
    stat = "success"
    bstat = "error"
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            if "zip" in file.filename:
                list_file = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], list_file))
                save = os.path.join(app.config["UPLOAD_FOLDER"], list_file)
                # extract all files and iterate through it.
                unpack_archive(save, folder)
                # if the zip is in this dir, delete it
                if os.path.isfile(save):
                    os.remove(save)
                if os.path.isdir(folder):
                    for name in os.listdir(folder):
                        # get a direct path to the secured file dir
                        z = os.path.join(folder, name)
                        # on macOs the file and other dir are auto
                        # create, we want to delete that as well
                        if ".zip" in z:
                            os.remove(z)
                        elif ".DS_Store" in z:
                            os.remove(z)
                        elif "__" in z:
                            os.rmdir(z)
                        else:
                            for names in os.listdir(z):
                                c = url_for("view", filename=names)
                                op = f"File has been uploaded link http://127.0.0.1:5000{c}"
                                msg = {"status": stat, "message": op}
                                show.append(msg)
                    return dict(results=show)
            else:
                # if one file is uploaded show that
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                c = url_for("view", filename=filename)
                op = f"File has been uploaded, check link at http://127.0.0.1:5000{c}"
                msg = dict(status=stat, message=op)
                return msg
        else:
            # if the format is wrong, mention that
            op = "File type not supported, only Images allowed"
            msg = dict(status=bstat, message=op)
            return msg
