## Курсовий проект "Моніторингова система ресурсів з продажами ноутбуків"

### Документація:
- [Технічне завдання](docs/ТЗ_Завгородня_КП72.docx)

### Масштабування бази даних:
#### Реплікація MongoDB з Replica set
Суть ReplicaSet полягає в тому, що різні репліки в собі зберігають однакові набори даних. Один сервер повинен виступати в якості основного сервера (на нього будуть надходити всі дані - він же ведучий, він же PRIMARY), а всі інші - є вторинними (вони зберігають копії даних з PRIMARY - вони ж SECONDARYs).

Для правильно роботиї ReplicaSet необхідно 3 запущених сервера з MongoDB:
- Одна нода виступатиме як арбітр і не братиме на себе ніякі дані. ЇЇ робота, полягає в тому, щоб вибрати того, хто буде сервером PRIMARY
- Один сервер виступає в якості PRIMARY сервера
- Один сервер виступає в якості SECONDARY сервера

##### Інструкція з репліціювання:
```shell
# Запускаємо сервер в якості PRIMARY (master)
mongod --dbpath /var/lib/mongo/my_database_1 --port 27001 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_1.log
# Запускаємо сервер в якості SECONDARY (slave):
mongod --dbpath /var/lib/mongo/my_database_2 --port 27002 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_2.log
# Запускаємо сервер в якості арбітра (який не зберігає даних):
mongod --dbpath /var/lib/mongo/my_database_3 --port 27003 --replSet My_Replica_Set --fork --logpath /var/log/mongodb/my_database_3.log
```
Налаштування PRIMARY сервера:
```shell
mongo --host 127.0.0.1 --port 27001
rs.initiate({"_id" : "My_Replica_Set", members : [ {"_id" : 0, priority : 3, host : "127.0.0.1:27001"}, {"_id" : 1, host : "127.0.0.1:27002"}, {"_id" : 2, host : "127.0.0.1:27003", arbiterOnly : true} ] });
```
В результаті налаштована MongoDB буде доступна за адресою `mongodb://127.0.0.1:27003`.

#### MongoDB sharding:
Шардована (shard - уламок) схема - схема, в якій дані не просто записуються в mongo чанки, які потім діляться навпіл, а потрапляють в чанки за певним діапазоном заданого поля - shard key. Спочатку створюється один чанк і діапазон значень, які приймає shard, він лежить в межах (-∞, + ∞). Коли розмір цього чанка досягає chunksize, mongos оцінює значення всіх shard keys всередині чанка і ділить чанк таким чином, щоб дані були розділені приблизно порівну.
##### Інструкція з шардування:
```shell
# Піднімаємо 2 інстанси mongod
mongod --dbpath /data/instance1 --port 27000 --fork --syslog
mongod --dbpath /data/instance2 --port 27001 --fork --syslog
# Піднімаємо конфіг сервер
mongod --configsvr --dbpath /data/config --port 27002 --fork --syslog
# Піднімаємо mongos
mongos --configdb 127.0.0.1:27002 --port 27100 --fork --syslog
``` 
Налаштування mongos:
```shell
mongo --port 27100
# додаємо 1 shard
sh.addShard("127.0.0.1:27000")
# додаємо 2 shard
sh.addShard("127.0.0.1:27001")
use admin
sh.enableSharding("course_work")
# вмикаємо шардування за полем price
db.runCommand({shardCollection: "course_work.laptops", key: {price: 1}})
# перевіряємо результат
db.printShardingStatus() 
```
В результаті налаштована MongoDB буде доступна за адресою `mongodb://127.0.0.1:27100`.

Авторка: [Анна Завгородня](https://t.me/tupoanka)