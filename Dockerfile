# base image 
FROM python:3.8

# File Author / Maintainer
LABEL  MAINTENER = aristidemassaga@gmail.com

#add project files to the usr/src/app folder
ADD ./webapp /usr/src/app

#set directoty where CMD will execute 
WORKDIR /usr/src/app

COPY requirements.txt ./

#install mysql
RUN apt update
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

# Get pip to download and install requirements:
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install mysqlclient

# Expose ports
EXPOSE 8000

# migration
python manage.py migrate

# copy static files
python manage.py collectstatic

# default command to execute    
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
