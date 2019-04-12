import os
import unittest

import dashboardFunctions
import testData

class dashboardViewsTests(unittest.TestCase):

	def test_dbCallData(self):
		indicentData = dashboardFunctions.indicentData
		TransferListDict = dashboardFunctions.TransferListDict
		extendedTransferListDict = dashboardFunctions.extendedTransferListDict
		chartData = dashboardFunctions.chartData
		montlyIncidentData = dashboardFunctions.montlyIncidentData
		queueIncidentData = dashboardFunctions.queueIncidentData
		extendedIncidentData = dashboardFunctions.extendedIncidentData

		dashboardFunctions.dbCallData()

		self.assertEqual(type(dashboardFunctions.indicentData), list)
		self.assertEqual(type(dashboardFunctions.TransferListDict), dict)
		self.assertEqual(type(dashboardFunctions.extendedTransferListDict), dict)
		self.assertEqual(type(dashboardFunctions.chartData), list)
		self.assertEqual(type(dashboardFunctions.montlyIncidentData), list)
		self.assertEqual(type(dashboardFunctions.queueIncidentData), list)
		self.assertEqual(type(dashboardFunctions.extendedIncidentData), list)

		self.assertNotEqual(dashboardFunctions.indicentData, None)
		self.assertNotEqual(dashboardFunctions.TransferListDict, None)
		self.assertNotEqual(dashboardFunctions.extendedTransferListDict, None)
		self.assertNotEqual(dashboardFunctions.chartData, None)
		self.assertNotEqual(dashboardFunctions.montlyIncidentData, None)
		self.assertNotEqual(dashboardFunctions.queueIncidentData, None)
		self.assertNotEqual(dashboardFunctions.extendedIncidentData, None)

	def test_dbCallDataTEST(self):
		resultIndicentData = testData.indicentData
		resultTransferListDict = testData.TransferListDict
		resultExtendedTransferListDict = testData.extendedTransferListDict
		resultChartData = testData.chartData
		resultMontlyIncidentData = testData.montlyIncidentData
		resultQueueIncidentData = testData.queueIncidentData
		resultExtendedIncidentData = testData.extendedIncidentData

		dashboardFunctions.dbCallDataTEST()

		self.assertEqual(dashboardFunctions.indicentData, resultIndicentData)
		self.assertEqual(dashboardFunctions.TransferListDict, resultTransferListDict)
		self.assertEqual(dashboardFunctions.extendedTransferListDict, resultExtendedTransferListDict)
		self.assertEqual(dashboardFunctions.chartData, resultChartData)
		self.assertEqual(dashboardFunctions.montlyIncidentData, resultMontlyIncidentData)
		self.assertEqual(dashboardFunctions.queueIncidentData, resultQueueIncidentData)
		self.assertEqual(dashboardFunctions.extendedIncidentData, resultExtendedIncidentData)

	def test_setTransferClasses(self):
		self.maxDiff = None
		expected = testData.extendedTransferListDict
		extendedIncidentData = testData.extendedIncidentData
		result = dashboardFunctions.setTransferClasses(extendedIncidentData)
		self.assertEqual(result, expected)

if __name__ == "__main__":
	unittest.main()