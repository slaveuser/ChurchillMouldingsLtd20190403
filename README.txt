README.txt

Install Dependencies:
	pip install reqirements.txt

Start Server:
	Development:
		python app.py

	Production:
		gunicorn -w 4 -b 0.0.0.0:5000 app:app --timeout 90

Add Queue:
	add queue to config.py
	add link in navtemplate.html
	in DB, table cs_pods_extended, add queue names
	restart server


