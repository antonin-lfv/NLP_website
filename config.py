# ===== Import
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, Flask
from werkzeug.utils import secure_filename
import os

# ===== Constants
ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'uploaded_files/data'


# ===== Functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
