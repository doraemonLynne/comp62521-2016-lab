from comp62521.statistics import average
import itertools
import operator
import numpy as np
import json
from xml.sax import handler, make_parser, SAXException

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]
LastNamePart = set(["van","der","de","du","al","el","da","Van","Der","De","Du","Al","El","Da"])
separation_checked_authors = []

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors

class Author:
    def __init__(self, name):
        self.name = name
        nameList = name.split()
        self.lastName = nameList[-1]
        self.firstName = nameList[0]
        if len(nameList) > 2:
            posLastNames = nameList[1:-1]
            for name in posLastNames:
                if name in LastNamePart:
                    self.lastName= name+" "+ self.lastName
                else:
                    self.firstName+= name+" "

class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])

        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)

    def get_publications_by_author(self):
        header = ["Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total"]

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [[self.authors[i].name]+ astats[i] + [sum(astats[i])] for i in range(len(astats))]
        dataIncludeLastName = [[self.authors[i].name]+ astats[i] + [sum(astats[i])] + [self.authors[i].lastName] for i in range(len(astats))]
        return (header, data, dataIncludeLastName)

    def get_author_search_details(self):
        header = ["Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total publications","Number of times first author","Number of times last author","Number of Sole-Authored Papers","Number of Co-Authors"]

        astatsPub = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astatsPub[a][p.pub_type] += 1

        coauthors = {}
        astatsAuthor = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                if len(p.authors)!=1:
                    if a==p.authors[0]:
                        astatsAuthor[a][0]+=1
                    if a==p.authors[-1]:
                        astatsAuthor[a][1]+=1
                elif len(p.authors)==1:
                    astatsAuthor[a][2]+=1
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                            astatsAuthor[a][3]=len(coauthors[a]);
                        except KeyError:
                            coauthors[a] = set([a2])

        data = [[self.authors[i].name]+ astatsPub[i] + [sum(astatsPub[i])] + astatsAuthor[i] for i in range(len(astatsPub))]
        dataIncludeLastName = [[self.authors[i].name]+ astatsPub[i] + [sum(astatsPub[i])] + astatsAuthor[i] + [self.authors[i].lastName] for i in range(len(astatsPub))]
        return (header, data, dataIncludeLastName)

    def get_author_details_publications_type(self,authorName):
        header = ("","overall","conference papers","journal articles","books","book chapters")

        coauthors = {}
        coauthor = [[0] for _ in range(len(self.authors))]
        apubstats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        afirstats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        alaststats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        asolestats = [[0, 0, 0, 0] for _ in range(len(self.authors))]

        for p in self.publications:
            for a in p.authors:
                apubstats[a][p.pub_type] += 1
                if len(p.authors)!=1:
                    if a==p.authors[0]:
                        afirstats[a][p.pub_type] += 1
                    if a==p.authors[-1]:
                        alaststats[a][p.pub_type] += 1
                elif len(p.authors)==1:
                    asolestats[a][p.pub_type] += 1
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                            coauthor[a][0]=len(coauthors[a])
                        except KeyError:
                            coauthors[a] = set([a2])
        apubdata = [[sum(apubstats[i])]+apubstats[i] for i in range(len(apubstats)) if self.authors[i].name==authorName]
        afirdata = [[sum(afirstats[i])]+afirstats[i] for i in range(len(afirstats)) if self.authors[i].name==authorName]
        alastdata = [[sum(alaststats[i])]+alaststats[i] for i in range(len(alaststats)) if self.authors[i].name==authorName]
        asoledata = [[sum(asolestats[i])]+asolestats[i] for i in range(len(asolestats)) if self.authors[i].name==authorName]
        coauthordata = [coauthor[i] for i in range(len(coauthor)) if self.authors[i].name==authorName]

        return (header, apubdata, afirdata, alastdata, asoledata, coauthordata)


    def get_author_search(self,searchText):
        collection = self.get_author_search_details()
        header=collection[0]
        data=collection[1]

        data=[data[i] for i in range(len(data)) if searchText.upper() in self.authors[i].name.upper()]

        return (header, data)

    def get_author_order(self,order,details):
        collection = details
        header=collection[0]
        data=collection[2]
        if order=="ascend":
            sortedData = sorted(data,key = lambda x:x[len(header)])
            sortedDataClipped =[]
        if order=="descend":
            sortedData = sorted(data,key = lambda x:x[len(header)],reverse=True)
            sortedDataClipped =[]

        for datum in sortedData:
            sortedDataClipped.append(datum[0:len(header)])

        return(header,sortedDataClipped)

    def get_col_order(self,col,order,details):
        preSortHeader, preSortData = self.get_author_order("ascend",details)
        collection=details
        header=tuple(preSortHeader)
        data=preSortData
        colNames=preSortHeader
        def by_colName(t):
            for i in range(len(colNames)):
                colNames[i]=colNames[i].replace(' ','')
                if colNames[i]==col:
                    return t[i]

        if order=="ascend":
            sortedData = sorted(data,key = by_colName)
        if order=="descend":
            sortedData = sorted(data,key = by_colName,reverse=True)

        return(header,sortedData)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        return (header, data)

    def get_author_totals_by_appearingtimes(self):
        header = ["Author", "Number of times first author", "Number of times last author",
        "Number of Sole-Authored Papers","Total"]

        astats = [ [0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                if len(p.authors)!=1:
                    if a==p.authors[0]:
                        astats[a][0]+=1
                    if a==p.authors[-1]:
                        astats[a][1]+=1
                elif len(p.authors)==1:
                    astats[a][2]+=1
        data = [ [self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        dataIncludeLastName = [ [self.authors[i].name] + astats[i] + [sum(astats[i])] + [self.authors[i].lastName]
        for i in range(len(astats)) ]
        return (header, data, dataIncludeLastName)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_coauthor_details_author_control(self, name, include_self):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, include_self)
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    def get_author_separation_degree(self, name1, name2, degree):
        pos_coauthors = self.get_coauthor_details_author_control(name1, False)
        pos_coauthor_names=[]
        for coauth in pos_coauthors:
            pos_coauthor_names.append(coauth[0])
        if not pos_coauthor_names:
            return False, -1
        if name2 in pos_coauthor_names:
            return True, degree
        else:
            degree+=1
            for coauth_name in pos_coauthor_names:
                if coauth_name in separation_checked_authors:
                    return False, -1
                else:
                    separation_checked_authors.append(coauth_name)
                    return self.get_author_separation_degree(coauth_name, name2, degree)
        del self.separation_checked_authors[:]
    
    def getAuthors(self):
        header=("Total Authors",)
        data = [[self.authors[i].name] for i in range(len(self.authors))]
        return (header,data)


class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""


    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
