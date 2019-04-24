
# to remove existing container, build and start new

git pull
sudo docker build -t graphql .
sudo docker stop graphql && sudo docker rm graphql
sudo docker run -d --name graphql -e MYSQL_ROOT_PASSWORD=biobakery -e MYSQL_USER=biom_mass -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=portal_ui -p 5000:5000 -v /opt/database:/var/lib/mysql graphql
