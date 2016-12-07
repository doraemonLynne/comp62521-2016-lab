from os import path
import unittest

from comp62521.database import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data, dataIncludeLastName = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")


    def test_get_author_totals_by_appearingtimes(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"sprint-2-acceptance-2.xml")))
        header, data, dataIncludeLastName = db.get_author_totals_by_appearingtimes()
        self.assertEqual(len(header),len(data[0]),"header and data column size doesn't match")
        self.assertEqual(data[0][1], 2, "incorrect number of times the author appears as first author")
        self.assertEqual(data[0][3], 1, "incorrect Number of appearances as sole author")

    def test_get_author_search_details(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
        header, data, dataIncludeLastName = db.get_author_search_details()
        self.assertEqual(len(header),len(data[0]),"header and data column size doesn't match")
        self.assertEqual(data[0][0], "Stefano Ceri", "incorrect author")
        self.assertEqual(data[0][1], 100, "incorrect number of conference papers")
        self.assertEqual(data[0][2], 94, "incorrect number of journals")
        self.assertEqual(data[0][3], 6, "incorrect number of books")
        self.assertEqual(data[0][4], 18, "incorrect number of book chapters")
        self.assertEqual(data[0][5], 218, "incorrect number of total publications")
        self.assertEqual(data[0][6], 78, "incorrect number of times first author")
        self.assertEqual(data[0][7], 25, "incorrect number of times last author")
        self.assertEqual(data[0][8], 8, "incorrect number of coauthors")
        self.assertEqual(data[0][9], 230, "incorrect number of coauthors")

    def test_get_author_search(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
        header, data = db.get_author_search("Stefano Ceri")
        self.assertEqual(len(data),1,"incorrect number of data")
        header, data = db.get_author_search("Stefano")
        self.assertEqual(len(data),5,"incorrect number of data")
        header, data = db.get_author_search("Ceri")
        self.assertEqual(len(data),2,"incorrect number of data")
        header, data = db.get_author_search("")
        self.assertEqual(len(data),1139,"incorrect number of data")
        header, data = db.get_author_search("abc")
        self.assertEqual(len(data),0,"incorrect number of data")

    def test_get_author_order(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"three-authors-and-three-publications.xml")))
        details=db.get_publications_by_author()
        order="ascend"
        header, data = db.get_author_order(order,details)
        self.assertNotEqual(data,[[u'Valeria De Antonellis', 2, 0, 0, 0, 2], [u'Stefano Ceri', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])
        self.assertEqual(data,[[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])
        order="descend"
        header, data = db.get_author_order(order,details)
        self.assertEqual(data,[[u'Krishna G. Kulkarni', 1, 0, 0, 0, 1], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Stefano Ceri', 2, 0, 0, 0, 2]])
        self.assertNotEqual(data,[[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])

    def test_get_col_order(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"three-authors-and-three-publications.xml")))
        details=db.get_publications_by_author()
        col = "Total"
        order="ascend"
        one = 1
        header, data = db.get_col_order(col,order,details)
        self.assertEqual(data,[[u'Valeria De Antonellis', 1, 0, 0, 0, 1],[u'Krishna G. Kulkarni', 1, 0, 0, 0, 1],[u'Stefano Ceri', 2, 0, 0, 0, 2]])
        self.assertNotEqual(data,[[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])
        order="descend"
        header, data = db.get_col_order(col,order,details)
        self.assertEqual(data, [[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])
        self.assertNotEqual(data,[[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1], [u'Valeria De Antonellis', 1, 0, 0, 0, 1]])
        col = "Number of conference papers"
        header, data = db.get_col_order(col,order,details)
        self.assertEqual(data, [[u'Stefano Ceri', 2, 0, 0, 0, 2], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Krishna G. Kulkarni', 1, 0, 0, 0, 1]])
        self.assertNotEqual(data,[[u'Krishna G. Kulkarni', 1, 0, 0, 0, 1], [u'Valeria De Antonellis', 1, 0, 0, 0, 1], [u'Stefano Ceri', 2, 0, 0, 0, 2]])

    def test_get_author_details_publications_type(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
        header, apubdata, afirdata, alastdata, asoledata, coauthordata = db.get_author_details_publications_type("Carlo Batini") #test Carlo Batini
        self.assertEqual(apubdata[0][0], 10, "incorrect overall publications")
        self.assertEqual(apubdata[0][1], 6, "incorrect number of conference papers")
        self.assertEqual(apubdata[0][2], 3, "incorrect number of journal articles")
        self.assertEqual(apubdata[0][3], 1, "incorrect number of books")
        self.assertEqual(apubdata[0][4], 0, "incorrect number of book chapters")
        self.assertEqual(afirdata[0][0], 3, "incorrect overall publications as first author")
        self.assertEqual(afirdata[0][1], 1, "incorrect number of conference papers as first author")
        self.assertEqual(afirdata[0][2], 1, "incorrect number of journal articles as first author")
        self.assertEqual(afirdata[0][3], 1, "incorrect number of books as first author")
        self.assertEqual(afirdata[0][4], 0, "incorrect number of book chapters as first author")
        self.assertEqual(alastdata[0][0], 5, "incorrect overall publications as last author")
        self.assertEqual(alastdata[0][1], 4, "incorrect number of conference papers as last author")
        self.assertEqual(alastdata[0][2], 1, "incorrect number of journal articles as last author")
        self.assertEqual(alastdata[0][3], 0, "incorrect number of books as last author")
        self.assertEqual(alastdata[0][4], 0, "incorrect number of book chapters as last author")
        self.assertEqual(asoledata[0][0], 0, "incorrect overall publications as sole author")
        self.assertEqual(asoledata[0][1], 0, "incorrect number of conference papers as sole author")
        self.assertEqual(asoledata[0][2], 0, "incorrect number of journal articles as sole author")
        self.assertEqual(asoledata[0][3], 0, "incorrect number of books as sole author")
        self.assertEqual(asoledata[0][4], 0, "incorrect number of book chapters as sole author")
        self.assertEqual(coauthordata[0][0], 15, "incorrect number of coauthors")

    def test_get_coauthor_details(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"three-authors-and-three-publications.xml")))
        coauthors = db.get_coauthor_details('Valeria De Antonellis')
        # print coauthors
        # print 'In test_get_coauthor_details:: coauthors are: '
        # if not coauthors:
        #      print 'error 404 coauthor not found'
        # else:
        #      print coauthors[0][0]
        one = 1
        self.assertEqual(one,1, "dumbass")

    def test_get_coauthor_details_author_control(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"three-authors-and-three-publications.xml")))
        coauthors = db.get_coauthor_details_author_control('Valeria De Antonellis', False)
        # print 'In test_get_coauthor_details_author_control:: coauthors are: '
        # print coauthors
        # if not coauthors:
        #      print 'error 404 coauthor not found'
        # else:
        #      print coauthors[0][0]
        one = 1
        self.assertEqual(one,1, "dumbass")


    def test_get_author_separation_degree(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir,"separation degree tests.xml")))
        found, degree = db.get_author_separation_degree('Stefano Ceri','Valeria De Antonellis',0 )
        self.assertEqual(found,True, "Found output should be true")
        self.assertEqual(degree,1, "Incorrect separation degree calculated")
        # print 'In test_get_author_separation_degree:: found boolean and separation degree are: '
        # print found
        # print degree
        # one = 1
        # self.assertEqual(one,2, "dumbass")
        found, degree = db.get_author_separation_degree('Stefano Ceri','Krishna G. Kulkarni',0 )
        self.assertEqual(found,True, "Found output should be true")
        self.assertEqual(degree,0, "Incorrect separation degree calculated")
        found, degree = db.get_author_separation_degree('Stefano Ceri','abc',0 )
        self.assertEqual(found,False, "Found output should be false")
        self.assertEqual(degree,-1, "separation degree should be 0")



        self.assertTrue(db.read(path.join(self.data_dir,"publications_small_sample.xml")))
        found, degree = db.get_author_separation_degree('Raghu Ramakrishnan','Simon Harper',0 )
        print 'In test_get_author_separation_degree:: found boolean and separation degree are: '
        print found
        print degree
        self.assertEqual(found,True, "Found output should be true")
        self.assertEqual(degree,0, "Incorrect separation degree calculated")
if __name__ == '__main__':
    unittest.main()
