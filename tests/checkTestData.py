import testData
exist = []
newTestData = []

for data in testData.extendedIncidentData:
	if not data[3] in exist:
		exist.append(data[3])
		newTestData.append(data)

print newTestData

