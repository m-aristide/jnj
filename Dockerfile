# base image 
FROM python:3.8

# File Author / Maintainer
LABEL  MAINTENER = aristidemassaga@gmail.com


#add project files to the usr/src/app folder
ADD ./webapp /usr/src/app

# add env
ADD ./env /usr/src/app

#set directoty where CMD will execute 
WORKDIR /usr/src/app

#source env
RUN source env/bin/active

# Expose ports
EXPOSE 8000

# default command to execute    
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
