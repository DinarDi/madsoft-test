# Установка
Склонировать репозиторий

    https://github.com/DinarDi/madsoft-test.git

Рядом с файлом docker-compose.yml создать:

    .env.pg и скопировать в него данные из .env.pg.example
    .env.minio и скопировать в него данные из .env.minio.example

Перейти в папку app_service

Создать
    
    .env.app и скопировать в него данные из .env.app.example

Перейти в папку media_service

Создать

    .env.app и скопировать в него данные из .env.app.example

Перейти к уровню, где находится файл docker-compose.yml

Поднять docker container

    docker-compose up -d --build

Применить миграции

    docker-compose exec -d app sh -c 'alembic upgrade head'

# Функциональность

Для просмотра документации перейти

    127.0.0.1:8000/docs

Для получения мемов надо отправить get запрос

    127.0.0.1:8000/api/v1/memes/   

Для получения одного мема надо отправить get запрос с id мема

    127.0.0.1:8000/api/v1/memes/{meme_id}

Для обновления мема надо отправить put запрос

    127.0.0.1:8000/api/v1/memes/{meme_id}

Для удаления мема надо отправить delete запрос

    127.0.0.1:8000/api/v1/memes/{meme_id}

При тестировании put запроса через docs надо убирать галочки с "Send empty value"