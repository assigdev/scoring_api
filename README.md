# Scoring Api

### Установка

Клонируем

    git clone https://github.com/assigdev/scoring_api.git

Requirements:

    python2
    
    pip install requirements.txt

### Запуск
    
C MemCached:
    
    docker-compose up -d memcached
    python api.py
    
C Redis:
    
    docker-compose up -d memcached
    python api.py -k redis

##### можно передать парамаетры при запуске

    python api.py --port 8080 --log log_filename

    python api.py -p 8080 -l log_filename


### Тестирование

для запуска тестов: 
    
    python tests.py

для запуска тестирования store:
    
    docker-compose up
    
    python test_store.py
