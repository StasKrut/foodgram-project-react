[![Foodgram Workflow](https://github.com/StasKrut/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/StasKrut/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

# Foodgram project
### Описание
Сервис «Продуктовый помощник»: приложение, в котором можно публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.

Адрес на внешнем серевере http://158.160.48.216/recipes


### Стек технологий использованный в проекте:
- Python 3.7
- Django 3.2.16
- DRF
- Docker
- Nginx
- Gunicorn
- PostgreSQL

### Запуск на удаленном сервере:
#### Клонирование репозитория

```bash
https://github.com/StasKrut/foodgram-project-react.git
```

#### Установка на сервере Docker, Docker Compose
```bash
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```
#### Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra
```bash
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```
#### Для работы с GitHub Actions необходимо в репозитории в разделе Secrets > Actions создать переменные окружения
```bash
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```
#### Создать и запустить контейнеры Docker, выполнить команду на сервере
```bash
sudo docker-compose up -d
```
#### Выполнить миграции, создать суперпользователя и собрать статику
```bash
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --noinput
```
#### Через админку импортировать ингредиенты из
```bash
data/ingredients.json
```
###Запуск проекта на локальной машине:
#### Клонирование репозитория

```bash
https://github.com/StasKrut/foodgram-project-react.git
```
#### В директории infra файл example.env переименовать в .env и заполнить своими данными:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ Django'
```
#### Создать и запустить контейнеры Docker, как указано выше.

#### После запуска проект будут доступен по адресу: http://localhost/

#### Документация будет доступна по адресу: http://localhost/api/docs/
  
Проект сделан в рамках учебного процесса по специализации Python-разработчик (backend) Яндекс.Практикум.

Автор в рамках учебного курса ЯП Python - разработчик:
- :white_check_mark: [Stanislav Krutskikh](https://github.com/StasKrut)
