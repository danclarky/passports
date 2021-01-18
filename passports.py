import csv
import psycopg2
import urllib3
from psycopg2 import sql
import os




def csv_dict_reader(file_obj,conn):
    reader = csv.DictReader(file_obj, delimiter=',')
    i=0
    u=0
    cursor = conn.cursor()
    with conn.cursor() as cursor:
        conn.autocommit = True
        delete = sql.SQL("delete from Паспорта")
        cursor.execute(delete)    
    for line in reader:
        if line["PASSP_SERIES"][:2] == '80':
            i+=1
            print(line["PASSP_SERIES"]+'  '+line["PASSP_NUMBER"])
            with conn.cursor() as cursor:
                conn.autocommit = True
                insert = sql.SQL("INSERT INTO Паспорта (Код) VALUES ('"+line["PASSP_SERIES"]+line["PASSP_NUMBER"]+"')")
                cursor.execute(insert)  
        u+=1
    print(i)    
    print(u)
    with conn.cursor() as cursor:
        conn.autocommit = True
        insert = sql.SQL("INSERT INTO ПришедшиеЗаявкиДляЗапроса (ФИО) VALUES ('Обновление паспортов закончилось.Кол-во:"+str(u)+", Колво: "+str(i)+"')")
        cursor.execute(insert) 
    
    
    
if __name__ == "__main__":
    conn = psycopg2.connect(dbname='Base', user='admin',password='pass', host='ip',port='port')
    cursor = conn.cursor()
    with conn.cursor() as cursor:
        conn.autocommit = True
        insert = sql.SQL("INSERT INTO ПришедшиеЗаявкиДляЗапроса (ФИО) VALUES ('Обновление паспортов началось')")
        cursor.execute(insert)  
                
    

  
        
    urllib3.disable_warnings()
    url = "http://guvm.mvd.ru/upload/expired-passports/list_of_expired_passports.csv.bz2"
    fileName ="D:/программа/passports/list_of_expired_passports.csv.bz2"
    with urllib3.PoolManager() as http:
        r = http.request('GET', url)
        with open(fileName, 'wb') as fout:
            fout.write(r.data)
   
    os.system("D:/программа/passports/7z.exe e D:/программа/passports/list_of_expired_passports.csv.bz2 -oD:/программа/passports")
   
    with open("D:/программа/passports/list_of_expired_passports.csv", encoding="utf8") as f_obj:
        csv_dict_reader(f_obj,conn)
os.remove("D:/программа/passports/list_of_expired_passports.csv.bz2")
os.remove("D:/программа/passports/list_of_expired_passports.csv")