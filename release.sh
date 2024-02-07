docker build -t registry.heroku.com/greekstudybuddy/web -f config/docker/Dockerfile.web . --platform linux/amd64
docker build -t registry.heroku.com/greekstudybuddy/node -f config/docker/Dockerfile.node . --platform linux/amd64
docker push registry.heroku.com/greekstudybuddy/node
docker push registry.heroku.com/greekstudybuddy/web
heroku container:release web node -a greekstudybuddy
