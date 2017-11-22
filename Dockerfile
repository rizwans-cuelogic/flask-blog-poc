 FROM faizanscuelogic/python-2.7
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /flask-blog-poc
 WORKDIR /flask-blog-poc
 COPY . /flask-blog-poc
 RUN rm -rf migrations
 RUN apt-get -y update
 RUN apt-get -y install curl wget make gcc build-essential
 ADD requirements.txt /flask-blog-poc/
 RUN pip install -r requirements.txt
 ADD . /flas-blog-poc/
 ADD /docker-entrypoint-initdb.d/init.sql /docker-entrypoint-initdb.d/
 RUN chmod u+x docker-entrypoint.sh
 ENTRYPOINT ["bash", "/flask-blog-poc/docker-entrypoint.sh"]
