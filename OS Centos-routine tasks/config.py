path_postgres = '/opt/pgpro/1c-12/bin/' #  Путь в формате указываем в формате
# C:\"Program Files"\"PostgreSQL 1C"\12\bin\ '\' обязательно!! и ""
user = 'postgres' # имя пользователя СУБД
password = 'password' # пароль пользователя СУБД
server = 'localhost' # IP сервера СУБД
port = '5432' # порт сервера СУБД
db = ['db1','db2'] # список баз
path_backup = '/mnt/backup/daily/' # путь хранения бекапов
shelf_life = '7' # срок хранения в днях
reindexdb = '1' # если 1 то выполнять реиндексацию, иначе не выполнять
vacuum = '1' # если 1 то выполнять vaccum, иначе не выполнять