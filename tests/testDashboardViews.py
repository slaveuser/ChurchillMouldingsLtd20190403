# project/test_basic.py

import os
import unittest

from app import app

TEST_DB = 'test.db'

class dashboardViewsTests(unittest.TestCase):

	############################
	#### setup and teardown ####
	############################

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
		# 	os.path.join(app.config['BASEDIR'], TEST_DB)
		self.app = app.test_client()
		# db.drop_all()
		# db.create_all()

		# Disable sending emails during unit testing
		self.assertEqual(app.debug, False)

	# executed after each test
	def tearDown(self):
		pass

###############
#### tests ####
###############

	def test_index(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_incidentFilter(self):
		response = self.app.get('/incidents/APLSUPBAL', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_selectQueues(self):
		response = self.app.get('/selectqueues', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_timeline(self):
		response = self.app.get('/timeline/CB454016', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_csc_q_count(self):
		response = self.app.get('/csc_q_count', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_nav(self):
		response = self.app.get('/nav', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_newdash(self):
		response = self.app.get('/newdash', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_newdashIncidents(self):
		response = self.app.get('/newdash/incidents/APLSUPBAL', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_stackedbar(self):
		response = self.app.get('/stackedbar', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_stackedbarqueue(self):
		response = self.app.get('/stackedbarqueue', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_requests(self):
		response = self.app.get('/requests', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
	unittest.main()