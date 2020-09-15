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
    colors = ['#FF6B6B', '#5BC0EB', '#ACF39D']
    

    # Plot
    patches, texts, autotexts=plt.pie(sizes,labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)

    for text in texts:
        text.set_color('grey')
    for autotext in autotexts:
        autotext.set_color('grey')


    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(img, format='png', transparent=True)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:images/png;base64,{}'.format(graph_url)


def build_trend_chart(topic):
    df = twitter.trendTweets(topic)
    img = io.BytesIO()
    labels = ['Negative', 'Positive', 'Neutral']
    neg = len([v for v in df['sentiment'] if v == -1])
    pos = len([v for v in df['sentiment'] if v == 1])
    nt = len([v for v in df['sentiment'] if v == 0])
    sizes = [neg, pos, nt]
    colors = ['#FF6B6B', '#5BC0EB', '#ACF39D']
    explode = (0, 0.1, 0)  # explode 1st slice

    # Plot
    patches, texts, autotexts=plt.pie(sizes,labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=90)

    for text in texts:
        text.set_color('grey')
    for autotext in autotexts:
        autotext.set_color('grey')

    plt.axis('equal')

    plt.savefig(img, format='png',transparent=True)
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

    plt.bar(y_pos, performance, align='center', alpha=0.5, color = ['#FF6B6B', '#5BC0EB'])
    plt.xticks(y_pos, objects)
    y= plt.ylabel('Number of Tweets')
    t= plt.title('Positive Tweets vs Negative Tweets')
    y.set_color("grey")
    t.set_color("grey")


    plt.savefig(img, format='png',transparent=True)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:images/png;base64,{}'.format(graph_url)


