from comp62521 import app
from database import database
from flask import (render_template, request)
from flask import Flask, jsonify, render_template, request

def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })

    args['tables'] = tables
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"

    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    return render_template("coauthors.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()

    #author_appearingtimes
    if (status == "author_appearingtimes"):
        args["title"] = "Author by AppearingTimes"
        args["data"] = db.get_author_totals_by_appearingtimes()

    return render_template('statisticsdetails.html', args=args)


@app.route("/statisticsdetails/publication_author_sortable")
def showPublicationSortable():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":"publication_author_sortable"}
    args["title"] = "Author Publication Sortable"
    args["data"] = db.get_publications_by_author()
    return render_template('statistics_details.html', args=args)


@app.route("/statisticsdetails/<status>/ascend")
def showAscend(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "Author"):
        args["title"] = "publication_author_ascend"
        args["data"] = db.get_author_ascend()

    if (status == "Papers"):
        args["title"] = "publication_papers_ascend"
        args["data"] = db.get_papers_ascend()

    if (status == "Journals"):
        args["title"] = "publication_journals_ascend"
        args["data"] = db.get_journals_ascend()

    if (status == "Books"):
        args["title"] = "publication_books_ascend"
        args["data"] = db.get_books_ascend()

    if (status == "Chapter"):
        args["title"] = "publication_chapter_ascend"
        args["data"] = db.get_chapter_ascend()

    if (status == "Total"):
        args["title"] = "publication_total_ascend"
        args["data"] = db.get_total_ascend()

    return render_template('statistics_details.html', args=args)

@app.route("/statisticsdetails/<status>/descend")
def showDescend(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "Author"):
        args["title"] = "publication_author_descend"
        args["data"] = db.get_author_descend()

    if (status == "Papers"):
        args["title"] = "publication_papers_descend"
        args["data"] = db.get_papers_descend()

    if (status == "Journals"):
        args["title"] = "publication_journals_descend"
        args["data"] = db.get_journals_descend()

    if (status == "Books"):
        args["title"] = "publication_books_descend"
        args["data"] = db.get_books_descend()

    if (status == "Chapter"):
        args["title"] = "publication_chapter_descend"
        args["data"] = db.get_chapter_descend()

    if (status == "Total"):
        args["title"] = "publication_total_descend"
        args["data"] = db.get_total_descend()

    return render_template('statistics_details.html', args=args)