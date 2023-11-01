from bluetooth import *
import pymysql

db = None
cur = None

backflow_minute = 0
distance_minute = 0

db = pymysql.connect(host='192.168.0.63', user='root', password='pi', db='mysql', charset='utf8')

try:
    cur = db.cursor()
    sql = "INSERT INTO COUNT(COUNT) VALUES (%d)" % (count)
    cur.execute(sql)
    db.commit()
    while True:
        msg = client_socket.recv(1024)
        print(msg)
        if msg == b'!':
            backflow_minute = backflow_minute + 1
        elif msg == b'@':
            distance_minute = distance_minute + 1
        elif msg == b'#':
            backflow_minute = 0
        elif msg == b'$':
            distance_minute = 0

        sql = "INSERT INTO backflow_distance(BACKFLOW_MINUTE,DISTANCE_MINUTE) VALUES (%d,%d)" % (backflow_minute, distance_minute)
        cur.execute(sql)
        db.commit()

    client_socekt.close()

except KeyboardInterrupt:
    pass

finally:
    db.close()
