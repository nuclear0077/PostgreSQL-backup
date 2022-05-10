import config  # импортируем наш конфиг
import os  # импортируем модуль для работы с ОС
import datetime  # импортируем модуль для работы со временем
import time  # переменная для времени


def start_backup(path_postgres, user, password, path_backup, db, server, port, reindexdb,
                 vacuum):  # функция для бекапирования
    path_backup = path_backup + db  # переменная для пути файла
    date = datetime.datetime.today()  # получаем дату и время
    date = date.strftime("%m_%d_%Y_%H_%M_%S_")  # формируем дату для имени
    file_name = date + db + '.backup'  # имя бекапа
    log_name = date + db + '.log'  # имя лога
    if os.path.exists(path_backup) == False:  # проверяем существует ли папка с название БД если папки нет то создаем
        os.mkdir(path_backup)
    command = path_postgres + 'pg_dump.exe' + ' ' + '--dbname=postgresql://' + user + ':' + password + '@' + server + ':' \
              + port + '/' + db + ' ' + '> ' + path_backup + '\\' + file_name + ' -v -F c 2> ' \
              + path_backup + '\\' + log_name  # формируем команду для бекапа
    os.system(command)
    # проверяем, если в конфиге 1 то выполняем реиндексацию баз
    if reindexdb == '1':
        # формируем наименование лога
        log_name = date + db + '_reindexdb.log'
        # формируем команду
        command_reindexdb = path_postgres + 'reindexdb.exe' + ' ' + '--dbname=postgresql://' + user + ':' + password + '@' + server + ':' \
                            + port + '/' + db + ' ' + ' -v 2> ' + path_backup + '\\' + log_name  # формируем команду для бекапа
        # исполняем команду
        os.system(command_reindexdb)
    # проверяем, если в конфиге 1 то выполняем очитску бд
    if vacuum == '1':
        # формируем наименование лога
        log_name = date + db + '_vacuum.log'  # имя лога
        # исполняем команду
        command_vacuum = path_postgres + 'vacuumdb.exe' + ' ' + '--dbname=postgresql://' + user + ':' + password + '@' + server + ':' \
                         + port + '/' + db + ' ' + ' -v 2> ' + path_backup + '\\' + log_name  # формируем команду для бекапа
        # выполняем команду
        os.system(command_vacuum)


now = time.time()  # текущее время
date = now - (int(config.shelf_life) * 86400)  # переменная для условия ( текущее время - X дней )

# цикл для выполнение бекапа по списку баз
for db in config.db:
    start_backup(config.path_postgres, config.user, config.password, config.path_backup, db, config.server, config.port,
                 config.reindexdb, config.vacuum)
    files = os.listdir(config.path_backup + db + '\\')  # директория с файлами
    for file in files:  # цикл для удаление бекапов старше X дней
        file = config.path_backup + db + '\\' + file  # получаем путь файла
        time = os.stat(file)  # проверяем время изменения файла
        if os.stat(file).st_mtime < now - int(config.shelf_life) * 86400:  # условие для удаление файла
            os.remove(file)  # Удаляем файл
