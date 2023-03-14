from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from tools import *

BLP_general = Blueprint('BLP_general', __name__,
                        template_folder='templates/general')


@BLP_general.route('/', methods=['GET', 'POST'])
def home():
    input_data = None
    figures = None
    statistics = None
    if request.method == "POST":
        if request.form.get("text_input"):
            input_data = request.form.get("text_input")
        else:
            input_file = request.files.get('file_input')
            # read txt file with numpy
            if input_file.filename.endswith('.txt'):
                input_data = input_file.read().decode('utf-8')

        # Work with input_data (NLTK and Gensim)
        lang = "english"  # language of the input data (for stopwords)
        input_data = input_data.lower()
        figures = [plot_number_of_words_for_each_amount_of_letters(input_data),
                   plot_wordcloud_most_frequent_words(input_data),
                   plot_wordcloud_most_frequent_adjectives_last_30(input_data),
                   plot_wordcloud_most_frequent_verbs_last_30(input_data),
                   plot_wordcloud_most_frequent_words_len_more_6(input_data),
                   plot_wordcloud_most_frequent_words_without_stopwords(input_data, lang),
                   plot_most_frequent_words_evolution(input_data, lang)]
        statistics = stats(input_data)

    return render_template('index.html', figures=figures, statistics=statistics, enumerate=enumerate)
