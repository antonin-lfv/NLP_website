from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
import numpy as np

BLP_general = Blueprint('BLP_general', __name__,
                        template_folder='templates/general')


@BLP_general.route('/', methods=['GET', 'POST'])
def home():
    input_data = None
    if request.method == "POST":
        if request.form.get("text_input"):
            input_data = request.form.get("text_input")
        else:
            input_file = request.files.get('file_input')
            # read txt file with numpy
            if input_file.filename.endswith('.txt'):
                input_data = input_file.read().decode('utf-8')

        # Work with input_data (NLTK and Gensim)
        print(input_data)

    return render_template('index.html')
