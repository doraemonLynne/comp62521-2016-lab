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

@app.route("/index/<status>")
def showIndexData(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset}

    if(status == "totalPub"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        return jsonify(totalPub=args["data"][1][0][1])
    if(status == "totalAuth"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        return jsonify(totalAuth=args["data"][1][1][1])
    if(status == "pubByYear"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publications_by_year()
        return jsonify(args=args)
    if(status == "authByYear"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_author_totals_by_year()
        return jsonify(args=args)
    

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        return render_template('summary.html', args=args)

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()
        return render_template('publicationYear.html', args=args)

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()
        return render_template('authorYear.html', args=args)

    return render_template('statisticsdetails.html', args=args)

@app.route("/statisticsdetails/author_appearingtimes")
def showAppearingTimes():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    col= request.args.get('col')
    order=request.args.get('order')
    args = {"dataset":dataset, "id":col and order}
    details=db.get_author_totals_by_appearingtimes()
    if col and order:
        if col=="Author":
            args["title"] = "Author"+"-"+order
            args["data"] = db.get_author_order(order,details)
        else:
            args["title"] = col+"-"+order
            args["data"] = db.get_col_order(col,order,details)
    else:
        args["title"] = "Author by AppearingTimes"
        args["data"] = db.get_author_totals_by_appearingtimes()

    return render_template('appearingTimesSortable.html', args=args)

@app.route("/statisticsdetails/publication_author_sortable")
def showPublicationSortable():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    col= request.args.get('col')
    order=request.args.get('order')
    args = {"dataset":dataset, "id":col and order}
    details=db.get_publications_by_author()
    if col and order:
        if col=="Author":
            args["title"] = "Author"+"-"+order
            args["data"] = db.get_author_order(order,details)
        else:
            args["title"] = col+"-"+order
            args["data"] = db.get_col_order(col,order,details)
    else:
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    return render_template('statisticsdetailsSortable.html', args=args)

@app.route("/statisticsdetails/author_search")
def showAuthorSearch():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    searchText= request.args.get('searchText')
    col=request.args.get('col')
    order=request.args.get('order')
    details=db.get_author_search_details()
    args = {"dataset":dataset, "id":"authorSearch"}
    if searchText:   
        args["title"] = "Author Search"
        args["data"] = db.get_author_search(searchText)
    elif col and order:
        if col=="Author":
            args["title"] = "Author"+"-"+order
            args["data"] = db.get_author_order(order,details)
        else:
            args["title"] = col+"-"+order
            args["data"] = db.get_col_order(col,order,details)
    else:
        args["title"] = "Author Search"
        args["data"] = db.get_author_search_details()
    return render_template('authorSearch.html', args=args)

@app.route("/statisticsdetails/authorDetailsPublicationType")
def showAuthorDetailsPubType():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    autherName=request.args.get('autherName')
    args = {"dataset":dataset, "id":"authorDetailsPubType"}
    if autherName:
        args["title"] = autherName
        args["data"] = db.get_author_details_publications_type(autherName)
        return render_template('authorDetails.html',args=args)
    else:
        args["title"] = "Author Search"
        args["data"] = db.get_author_search_details()
        return render_template('authorSearch.html', args=args)









