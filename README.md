# dockerized_django_postgre_boilerplate
boilerplate for creating dockerized django app real quick

How to use it

#NOTE: you should have docker installed and running locally!

1. Clone this repo on locally
2. Navigate to root directory where docker-compose file is
3. Add or edit requirments.txt file to manipulate packages
4. Run command  "docker-compose build" - create image for us 
        (python:alpine, postgre:alpine, pillow, jpeg)
5. Run command - docker-compose run app sh -c "django-admin.py startproject app ."
6. To start app - run command "docker-compose up" )) Happy coding! 

'app' is name of your service in Dockerfile
'sh -c' is for separating docker command and image container command where linux ubuntu
