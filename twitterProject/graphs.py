import matplotlib.pyplot as plt
import io
import base64
from twitterProject import twitter
import numpy as np


def build_pie_chart(name):
    df = twitter.tweets(name)
    img = io.BytesIO()
    labels = ['Negative', 'Positive', 'Neutral']
    neg = len([v for v in df['sentiment'] if v == -1])
    pos = len([v for v in df['sentiment'] if v == 1])
    nt = len([v for v in df['sentiment'] if v == 0])
    sizes = [neg, pos, nt]
    colors = ['red', 'blue', 'grey']
    explode = (0, 0.1, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')

    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:images/png;base64,{}'.format(graph_url)


def build_bar_chart(name):
    df = twitter.tweets(name)
    neg = len([v for v in df['sentiment'] if v == -1])
    pos = len([v for v in df['sentiment'] if v == 1])
    img = io.BytesIO()
    objects = ('Negative', 'Positive')
    y_pos = np.arange(len(objects))
    performance = [neg, pos]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Number of Tweets')
    plt.title('Positive Tweets vs Negative Tweets')
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:images/png;base64,{}'.format(graph_url)


def build_trend_chart(loc):
    img = io.BytesIO()
    objects = set(loc)
    y_pos = np.arange(len(objects))
    performance = []
    countries = {}
    for country in objects:
        num = loc.count(country)
        # countries[country] = num
        performance.append(num)

    countries
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Number of Tweets')
    plt.title('Number of Tweets per Country')

    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:images/png;base64,{}'.format(graph_url)
