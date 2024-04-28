docker build -t app-recipes:1.0.0 .
docker run -d -p 5001:5001 app-recipes:1.0.0