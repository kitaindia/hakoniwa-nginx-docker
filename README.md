# hakoniwa-nginx-docker
箱庭諸島2をnginxで動かす

docker build --build-arg BASE_DIR="http://localhost:5000" --build-arg IMAGE_DIR="http://localhost:5000/images" --build-arg MASTER_PASSWORD="password" --build-arg SPECIAL_PASSWORD="specielpassword" --build-arg ADMIN="admin" --build-arg EMAIL="admin@example.com" --build-arg BBS="http://localhost:5000" --build-arg TOPPAGE="http://localhost:5000" -t hakoniwa .

docker run -d -p 5000:80 hakoniwa

Access localhost:5000/hako-mente.cgi