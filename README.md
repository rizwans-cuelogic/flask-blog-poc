# flask-blog-poc
Flask Microblogging PlatForm.

For running application follow steps given below:
	
	1. create virtualenv and activate it as follows:
		virtualenv venv
		source venv/bin/activate
		
	2. pip install -r requirements.txt.
	3. create database blog and blog_test in postgresql with user postgres.
	4. change url of database in config.py as per your database,username 
	3. python run.py 


For running Test:

	1. run  python -m unittest app.tests.tests command.


For Running app in dockerized containers:
	
	1.update SQLALCHEMY_DATABASE_URI in congig.py as follows:
		replace localhost with flaskapp-postgres
		add database name as postgres

	2.run docker-compose up --build			 	