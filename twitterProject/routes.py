from flask import render_template, url_for, flash, redirect, request, abort
from twitterProject import app
from twitterProject.forms import SearchForm, TrendForm
from twitterProject.graphs import build_pie_chart, build_bar_chart, build_trend_chart
from twitterProject import twitter


@app.route("/")
@app.route("/landing", methods=['GET', 'POST'])
def landing():

    return render_template('landing.html')

@app.route("/results", methods=['GET', 'POST'])
def results():
    form = SearchForm()
    if form.validate_on_submit:
        name = form.name.data
        df = twitter.tweets(name)
        if not df.empty:
            piechart = build_pie_chart(name)
            barchart = build_bar_chart(name)
            return render_template('results.html', graph1=piechart, graph2=barchart, name=name, tweets=df['tweets'])
        else:
            flash('Uh oh, is that username correct?','danger')
            return redirect(url_for('home'))
    
    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    trendform = TrendForm()
    
    return render_template('home.html', form=form, trendform=trendform)



@app.route("/trendResults", methods=['GET', 'POST'])
def trendResults():
    trendform = TrendForm()
    
    if trendform.validate_on_submit():
        topic = trendform.trend.data
        df = twitter.trendTweets(topic)
        piechart = build_trend_chart(topic)

        return render_template('results.html', graph1=piechart, tweets=df['tweets'], topic=topic)
    
    return redirect(url_for('home'))



