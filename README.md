 # 🛠 Установка и настройка проекта
1. Клонируйте репозиторий на свой локальный компьютер.
```.sh
git clone <https://.git>
```
2. Создайте ``` config.ini ``` и добавьте ключи своих брокеров
```
    # Redis
    RESID_HOST=192.168.128.2
    REDIS_PORT=6379

    #PostgreSQL

    DB_HOST=pgdb
    DB_PORT=5432
    DB_NAME=dev
    USERNAME=root
    PASSWORD=root
    PGADMIN_DEFAULT_EMAIL=root@root.com
    PGADMIN_DEFAULT_PASSWORD=root

    # Server
    SERVER_PROTOCOL=http
    SERVER_PORT=8080
    SERVER_HOST=
    ENABLE_LOGGING=true

```
3. Установите необходимые зависимости, запустив команду:
```.sh
❯ pip install -r requirements.txt
or
❯ poetry install
```
4. Отдельно установить ta-lib
* ## Для Linux:
```.sh
❯ chmod +x talib.sh
❯ ./talib.sh
```
* ## Для Windows:
1. Скачать и установить библиотеку  ta-lib  ZIP-файлом по ссылке: https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-msvc.zip/download?use_mirror=deac-fra
2. Разархивировать архив в диск С: по пути: ``` C:\ta-lib ```
3. Скачать и установить Visual Studio Community (2015 и позже)- при установке VSC обязательно поставить галочку рядом с  "Разработка на С++" и "Мобильная разработка на С++" 
4. Запустить из панели "Пуск" Native Tools Command Prompt for VS...
5. Прописать путь:``` C:\ta-lib\c\make\cdr\win32\msvc ```
6. Прописать команду ``` nmake ```
7. В терминале PyCharm прописать команду ``` pip install ta-lib ``` (для проверки)

5. Start docker with PostgreSQL Database
```.sh
# clear docker cache
❯ sudo docker stop $(sudo docker ps -a -q)
❯ sudo docker rm $(sudo docker ps -a -q)
# Up postgresql database in docker
❯ docker-compose -f database.yaml build
❯ docker-compose -f database.yaml up
``` 

6.  Change database IP
```.sh
❯ docker inspect pgdb | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.22.0.2",
``` 

### Настройка pre-committer
```.sh
$ pre-commit migrate-config
Configuration has been migrated.
$ pre-commit run flake8 --all-files
flake8...................................................................Passed
```
