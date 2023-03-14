import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import en_core_web_sm
import plotly.io as pio
import nltk
import numpy as np
from PIL import Image
import plotly
import json
from collections import defaultdict, Counter
import re


def number_of_words_for_each_amount_of_letters(texte):
    """
    Count the number of words for each amount of letters
    :return: list of (amount of letters, number of words) sorted by index
    """
    # count the number of words for each amount of letters in a dictionary
    words = defaultdict(int)
    for word in texte.split():
        words[len(word)] += 1
    words = sorted(words.items())
    return words


def get_most_frequent_words(texte):
    """
    Get the most frequent words
    :return: list of tuples (word, number of occurences)
    """
    # Get the more frequent words
    words = re.findall(r'\w+', texte.lower())
    return Counter(words).most_common()


def stats(texte):
    # count the number of words
    words = re.findall(r'\w+', texte)
    nb_words = len(words)
    # count unique words
    unique_words = set(words)
    nb_unique_words = len(unique_words)
    return [nb_words, nb_unique_words]


def plot_number_of_words_for_each_amount_of_letters(texte):
    fig = None
    try:
        words = number_of_words_for_each_amount_of_letters(texte)
        # create a bar chart with the number of words for each amount of letters with plotly
        fig = go.Figure(data=[go.Bar(x=[x[0] for x in words], y=[x[1] for x in words])])
        fig.update_layout(xaxis_title="Nombre de lettres",
                          yaxis_title="Occurences")
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_number_of_words_for_each_amount_of_letters: ", e)
    return [fig, "Occurences des mots par nombre de lettres"]


def plot_wordcloud_most_frequent_words(texte):
    fig = None
    try:
        words = get_most_frequent_words(texte)
        # only keep the 30 most frequent words that have no special characters
        words = [x for x in words if x[0].isalpha()]
        words = words[:30]
        # create a word cloud with the most frequent words with wordcloud, given a list of tuples (word, frequency)
        wc = WordCloud(width=1200, height=600, background_color="white", prefer_horizontal=1, min_font_size=10, max_font_size=300)
        wc.generate_from_frequencies(dict(words))
        img_array = wc.to_array()
        fig = go.Figure(data=[go.Image(z=img_array)])
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_words: ", e)
    return [fig, "Nuage de mots des mots les plus fréquents"]


def plot_wordcloud_most_frequent_words_len_more_6(texte):
    fig = None
    try:
        words = get_most_frequent_words(texte)
        # only keep the most frequent words that have more than 6 letters and no special characters
        words = [(word, freq) for word, freq in words if len(word) >= 6 and word.isalpha()]
        words = words[:30]

        # create a word cloud with the most frequent words with wordcloud, given a list of tuples (word, frequency)
        wordcloud = WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(dict(words))

        # create a plotly figure and return its JSON representation
        fig = go.Figure(data=[go.Image(z=wordcloud.to_array())])
        fig.update_layout(xaxis_title=None,
                          yaxis_title=None,
                          xaxis_visible=False,
                          yaxis_visible=False)
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_words_len_more_6: ", e)
    return [fig, "Nuage de mots des mots les plus fréquents de taille supérieure ou égale à 6"]


def verbs(texte):
    """
    Get the verbs of the text
    :return: list of verbs
    """
    nlp = en_core_web_sm.load()
    doc = nlp(texte)
    verbs_list = [token.text for token in doc if token.pos_ == "VERB"]
    return verbs_list


def plot_wordcloud_most_frequent_verbs_last_30(texte):
    fig = None
    try:
        verbs_list = verbs(texte)
        # count the number of occurences of each verb using Counter
        verbs_occur = Counter(verbs_list)
        verbs_occur = verbs_occur.most_common(30)
        # only keep the 30 most frequent verbs that have no special characters
        verbs_occur = [x for x in verbs_occur if x[0].isalpha()]
        wordcloud = WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(dict(verbs_occur))
        fig = go.Figure(data=[go.Image(z=wordcloud.to_array())])
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_verbs_last_30: ", e)
    return [fig, "Nuage de mots des 30 verbes les plus fréquents"]


def common_nouns(texte):
    """
    Get the common nouns of the text
    :return: list of common nouns
    """
    nlp = en_core_web_sm.load()
    doc = nlp(texte)
    nouns_list = [token.text for token in doc if token.pos_ == "NOUN"]
    return nouns_list


def plot_wordcloud_most_frequent_common_nouns_last_30(texte):
    fig = None
    try:
        # get common nouns from the text
        nouns_list = common_nouns(texte)
        # count the number of occurrences of each noun and keep only the 30 most frequent
        nouns_occur = Counter(nouns_list).most_common(30)
        # create the word cloud
        wordcloud = WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(
            dict(nouns_occur))
        # create the plotly figure
        fig = go.Figure(data=[go.Image(z=wordcloud.to_array())])
        fig.update_layout(xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
        # encode the figure in JSON format
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_common_nouns_last_30: ", e)
    return [fig, "Nuage de mots des 30 noms communs les plus fréquents"]


def adjectives(texte):
    """
    Get the adjectives of the text
    :return: list of adjectives
    """
    nlp = en_core_web_sm.load()
    doc = nlp(texte)
    adjectives_list = [token.text for token in doc if token.pos_ == "ADJ"]
    return adjectives_list


def plot_wordcloud_most_frequent_adjectives_last_30(texte):
    fig = None
    try:
        adjectives_list = adjectives(texte)
        # count the number of occurences of each adjective
        adjectives_occur = Counter(adjectives_list)
        # only keep the 30 most frequent adjectives that have no special characters
        adjectives_occur = [x for x in adjectives_occur.most_common() if x[0].isalpha()][:30]
        wordcloud = WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(
            dict(adjectives_occur))
        fig = go.Figure(data=[go.Image(z=wordcloud.to_array())])
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_adjectives_last_30: ", e)
    return [fig, "Nuage de mots des 30 adjectifs les plus fréquents"]


def plot_wordcloud_most_frequent_words_without_stopwords(texte, lang):
    fig = None
    try:
        stopwords = set(nltk.corpus.stopwords.words(lang))
        words = [(word, freq) for word, freq in get_most_frequent_words(texte) if word.lower() not in stopwords and len(word) > 2]
        wordcloud = WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(dict(words))
        fig = go.Figure(data=[go.Image(z=wordcloud.to_array())])
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_wordcloud_most_frequent_words_without_stopwords: ", e)
    return [fig, "Nuage de mots des mots les plus fréquents en enlevant les mots vides et les mots de moins de 2 "
                 "lettres"]


def plot_most_frequent_words_evolution(texte, lang):
    fig = None
    try:
        # get the most frequent words
        words = get_most_frequent_words(texte)
        # remove stopwords
        stopwords = nltk.corpus.stopwords.words(lang)
        words = [x for x in words if x[0] not in stopwords]
        # remove words with less than 2 letters
        words = [x for x in words if len(x[0]) > 2]
        # keep only the 5 most frequent words
        words = words[:10]
        # get the 10% of the text
        text_10_percent = len(texte) // 10
        # get the 5 most frequent words evolution
        words_evolution = []
        for word in words:
            word_evolution = []
            for i in range(10):
                word_evolution.append(texte[i * text_10_percent:(i + 1) * text_10_percent].count(word[0]))
            words_evolution.append(word_evolution)
        # plot the evolution of the 5 most frequent words with plotly and splines interpolation
        fig = go.Figure()
        for i in range(len(words)):
            fig.add_trace(
                go.Scatter(x=np.linspace(0, 100, 10), y=words_evolution[i], name=words[i][0], mode="lines+markers",
                           line=dict(shape="spline")))
        fig.update_layout(xaxis_title="Partie du texte (%)", yaxis_title="Nombre d'apparition du mot")
        fig = pio.to_json(fig)
    except Exception as e:
        print("Error in plot_most_frequent_words_evolution: ", e)
    return [fig, "Évolution des 10 mots les plus fréquents sur chaque partie du texte"]


if __name__ == '__main__':
    lang = "english"
    texte = "The quick brown fox jumps over the lazy dog. pretty, cool, is, leave, jgqziefgvahkzeg " \
            "fgefug, lhqgeUFDYGZUEYGFOZEUF,"
    plot_number_of_words_for_each_amount_of_letters(texte)
    plot_wordcloud_most_frequent_words(texte)
    plot_wordcloud_most_frequent_words_len_more_6(texte)
    plot_wordcloud_most_frequent_verbs_last_30(texte)
    plot_wordcloud_most_frequent_common_nouns_last_30(texte)
    plot_wordcloud_most_frequent_adjectives_last_30(texte)
    plot_wordcloud_most_frequent_words_without_stopwords(texte, lang)
    plot_most_frequent_words_evolution(texte, lang)
