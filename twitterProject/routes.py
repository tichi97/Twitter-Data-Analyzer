from flask import render_template, url_for, flash, redirect, request, abort
from twitterProject import app
from twitterProject.forms import SearchForm, TrendForm
from twitterProject.graphs import build_pie_chart, build_bar_chart, build_trend_chart
from twitterProject import twitter


@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == "POST":
        name = request.form["name"]
        # name = "jackieaina"
        df = twitter.tweets(name)
        piechart = build_pie_chart(name)
        barchart = build_bar_chart(name)
        return render_template('results.html', graph1=piechart, graph2=barchart, name=name, tweets=df['tweets'])
    else:
        return redirect(url_for('home'))


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('results'))
    return render_template('home.html', form=form)


@app.route("/trends", methods=['GET', 'POST'])
def trends():
    form = TrendForm()
    action = "trends"
    return render_template('home.html', form=form, action=action)


@app.route("/trendResults", methods=['GET', 'POST'])
def trendResults():
    if request.method == "POST":
        topic = request.form["name"]
        # name = "jackieaina"
        tweets, loc, dates = twitter.trendTweets(topic)
        graph1 = build_trend_chart(loc)
        return render_template('results.html', graph1=graph1, tweets=tweets, topic=topic)
    else:
        return redirect(url_for('home'))
