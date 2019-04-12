# project/test_basic.py

import os
import unittest

from app import app

TEST_DB = 'test.db'

class gameViewsTests(unittest.TestCase):

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



	###############################
			#TEST WRAPPERS
	###############################



	def test_scoreboardAbout(self):
		response = self.app.get('/scoreboard/about', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	############ POST method ############
	# def changeTeam(self, EIN, team):
	# 	return self.app.post('/scoreboard/changeteam', data=dict(
	# 		EIN=EIN,
	# 		team=team
	# 	), follow_redirects=True)

	# def test_changeTeam(self):
	# 	response = self.changeTeam('61179372','UKRVASCOLO')
	# 	self.assertEqual(response.status_code, 200)
		
	def test_changeuser(self):
		response = self.app.get('/scoreboard/changeuser', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_activityfeed(self):
		response = self.app.get('/activityfeed', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboard(self):
		response = self.app.get('/scoreboard', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardDate(self):
		response = self.app.get('/scoreboard/date', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardWeek(self):
		response = self.app.get('/scoreboard/week', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardMonth(self):
		response = self.app.get('/scoreboard/month', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardRange(self):
		response = self.app.get('/scoreboard/range', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardTeam(self):
		response = self.app.get('/scoreboard/team', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardTeamDate(self):
		response = self.app.get('/scoreboard/team/date', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardTeamWeek(self):
		response = self.app.get('/scoreboard/team/week', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardTeamMonth(self):
		response = self.app.get('/scoreboard/team/month', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_scoreboardTeamRange(self):
		response = self.app.get('/scoreboard/team/range', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	############ POST method ############
	# def test_savedHours(self):
	# 	response = self.app.get('/scoreboard/entersavedhours', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)

	############ POST method ############
	# def test_proactiveP3(self):
	# 	response = self.app.get('/scoreboard/proactivep3', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	
	############ POST method ############
	# def test_rootCause(self):
	# 	response = self.app.get('/scoreboard/rootcause', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	
	def test_enterEIN(self):
		response = self.app.get('/enterEIN', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	############ POST method ############
	# def test_enterPassword(self):
	# 	response = self.app.get('/enterPassword', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	# self.assertEqual(response.status_code, 200)
	
	############ POST method ############
	# def test_createSession(self):
	# 	response = self.app.get('/createSession', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	# self.assertEqual(response.status_code, 200)
	
	############ POST method ############
	# def test_userSearch(self):
	# 	response = self.app.get('/scoreboard/user', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	
	############ POST method ############
	# def test_changeTheme(self):
	# 	response = self.app.get('/scoreboard/changeTheme', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	
	############ POST method ############
	# def test_form(self):
	# 	response = self.app.get('/form', follow_redirects=True)
	# 	self.assertEqual(response.status_code, 200)
	

if __name__ == "__main__":
	unittest.main()