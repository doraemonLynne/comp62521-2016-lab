
from comp62521 import app
import unittest
from os import path
from comp62521.database import database

class TestDatabase(unittest.TestCase):
	def setUp(self):
		db = database.Database()
		dir, _ = path.split(__file__)
		self.data_dir = path.join(dir,"..","data")
	
	def  trearDown(self):
		pass
	
	def test_read(self):
		db = database.Database()
		self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
		self.assertEqual(len(db.publications),932)

	
	def test_get_publication_summary(self):
		db = database.Database()
		self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
		header, data = db.get_publication_summary()
		self.assertEqual(len(header),len(data[0]),
			"header and data column size doesn't match")
		self.assertEqual(len(data[0]),6,
			"incorrect number of column in data")
	
	def test_get_publications_by_author(self):
		db = database.Database()
		self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
		header, data = db.get_publications_by_author()
		self.assertEqual(len(header),len(data[0]),
			"header and data column size doesn't match")
		self.assertEqual(len(data),1139,
			"incorrect number of authors")
		self.assertEqual(data[0][-1],218,
			"incorrect total")
	
	def test_get_publications_by_author_for_lName_sorting(self):
		db = database.Database()
		self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
		header, data = db.get_publications_by_author_for_lName_sorting()
		self.assertEqual(len(data[0]),8,
			"the value of sortedDataClipped isn't correct")
	
	# def test_get_papers_ascend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_papers_ascend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")

	# def test_get_journals_ascend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_journals_ascend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][2],0,
	# 		"the value of data isn't correct")

	# def test_get_books_ascend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_books_ascend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value ofsortedData isn't correct")
	# 	self.assertEqual(data[0][4],1,
	# 		"the value ofsortedData isn't correct")

	# def test_get_chapter_ascend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_chapter_ascend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][4],0,
	# 		"the value ofsortedData isn't correct")

	# def test_get_total_ascend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_total_ascend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][4],0,
	# 		"the value ofsortedData isn't correct")

	# def test_get_author_descend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_author_descend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][4],0,
	# 		"the value ofsortedData isn't correct")

	# def test_get_papers_descend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_papers_descend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[2][3],6,
	# 		"the value ofsortedData isn't correct")

	# def test_get_journals_descend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_journals_descend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[3][3],1,
	# 		"the value ofsortedData isn't correct")

	# def test_get_books_descend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_books_descend()
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][1],100,
	# 		"the value ofsortedData isn't correct")

	# def test_get_chapter_descend(self):
	# 	db = database.Database()
	# 	self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
	# 	header, data = db.get_chapter_descend();
	# 	self.assertEqual(len(data[0]),6,
	# 		"the value of sortedData isn't correct")
	# 	self.assertEqual(data[0][1],100,
	# 		"the value ofsortedData isn't correct")

	def test_get_author_totals_by_appearingtimes(self):
		db = database.Database()
		self.assertTrue(db.read(path.join(self.data_dir,"dblp_curated_sample.xml")))
		header, data = db.get_author_totals_by_appearingtimes()
		self.assertEqual(len(header),len(data[0]),
			"header and data column size doesn't match")
		self.assertEqual(data[0][1], 86,
            "incorrect number of authors in result")



if __name__ == '__main__':
	unittest.main()