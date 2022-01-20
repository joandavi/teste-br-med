Para executar o app siga os passos:

1. Clone este repositorio

2. Suba os containers:

`sudo docker-compose up`

3. Aplique as migracoes

`sudo docker-compose exec web python manage.py migrate`

4. Acesse http://localhost:8080/