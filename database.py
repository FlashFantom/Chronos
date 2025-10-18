import sqlite3
import nicegui
import math
from collections import OrderedDict
from datetime import datetime, time, timedelta

class Pool:
    def __init__(self):
        self.conn = sqlite3.connect('checkins.db')
        self.cursor = self.conn.cursor()


    def add_manager(self, name):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {name} (
                timestamp TIMESTAMP,
                state VARCHAR(20) CHECK (state IN ('Перерыв', 'На рабочем месте')),
                PRIMARY KEY (timestamp)
            );
        ''')


    def fetch_tables(self):
        sql_query = """SELECT name FROM sqlite_master  
        WHERE type='table';"""
        res = []
        tables = self.cursor.execute(sql_query).fetchall()
        for i in range(len(tables)):
            if (tables[i][0]!='leaves'):
                res.append(tables[i][0])
        return res
        


    def insert_data(self, name:str, time:str, state:str):
        self.cursor.execute(f"INSERT INTO {name} (timestamp, state) VALUES (?, ?)", (time, state))
        self.conn.commit()


    def fetch_start_time(self, name: str):
        return self.cursor.execute(f'''select time(timestamp)
            from {name}
            where date(timestamp)=date('now')
            limit 1
            ''').fetchone()[0]
    
    def fetch_out_duration(self, name:str, date='now') -> list:
        result = self.cursor.execute(f'''
                SELECT
                *
                FROM
                    {name}
                WHERE
                    date(timestamp) = date('{date}')
            ''').fetchall()
        sum = 0.0
        for i in range(len(result)):
            if (i>0 and result[i-1][1]=='Перерыв'):
                sum+=(datetime.fromisoformat(result[i][0])-datetime.fromisoformat(result[i-1][0])).total_seconds()

        sum = 3600 - sum
        minutes, seconds = divmod(int(sum), 60)
        minutes = int(int(sum)/60)
        if (sum<0):
            seconds = int(int(sum)%-60)*-1
        else:
            seconds = int(int(sum)%60)
        time_format = f"{minutes:02}:{seconds:02}"
        return time_format
    
    def fetch_out_duration_seconds(self, name:str, date='now') -> list:
        result = self.cursor.execute(f'''
                SELECT
                *
                FROM
                    {name}
                WHERE
                    date(timestamp) = date('{date}')
            ''').fetchall()
        sum = 0
        for i in range(len(result)):
            if (i>0 and result[i-1][1]=='Перерыв'):
                sum+=(datetime.fromisoformat(result[i][0])-datetime.fromisoformat(result[i-1][0])).total_seconds()
        return sum
    
    def fetch_state(self, english_name, real_name):
        sql = f'''select strftime('%d', timestamp) as day, max(time(timestamp)), manager
                from leaves
                where date(timestamp) = date('now') and manager COLLATE NOCASE = ?
                group by day, manager
                                '''
        
        try:
            result = self.cursor.execute(sql, (real_name,)).fetchall()
            if result:
                return "Уход"
        except sqlite3.OperationalError:
            return
        
        res = self.cursor.execute(f'''select state
                                    from {english_name}
                                    where date(timestamp) = date('now')
                                    order by timestamp desc
                                    limit 1
                                ''').fetchone()
        if res:
            return res[0]


    
    def get_check_ins(self, month: int, year: int = datetime.now().year):
        month = str(month).zfill(2)
        dashboard = {}
        
        for table in self.fetch_tables():
            if table in ['leaves', 'busy_status']:
                continue
            m_table = self.cursor.execute(
                f'''
                    select strftime('%d', timestamp) as day, min(timestamp)
                    from {table}
                    where strftime('%m', timestamp) = '{month}' and strftime('%Y', timestamp) = '{year}'
                    group by day
                '''
            ).fetchall()
            
            for day in m_table:       
                dashboard.setdefault(day[0], {})[table] = day[1]

        # Sorting by day (keys of dashboard) and returning an OrderedDict
        return OrderedDict(sorted(dashboard.items(), key=lambda x: int(x[0])))

    def fetch_check_outs(self, name, month:int, year:int=datetime.now().year) -> dict:
        month = str(month).zfill(2)

        sql = f'''
                    select strftime('%d', timestamp) as day
                    from {name}
                    where strftime('%m', timestamp) = '{month}' and strftime('%Y', timestamp) = '{year}'
                    group by day
                '''
        data = self.cursor.execute(sql).fetchall()
        row = {}
        for date in data:
            result = self.cursor.execute(f'''select *
            from {name}
            where strftime('%d', timestamp)='{date[0]}' and strftime('%m', timestamp)='{month}' and strftime('%Y', timestamp) = '{year}'
            ''').fetchall()
            sum = 0
            for i in range(len(result)):
                if (i>0 and result[i-1][1]=='Перерыв'):
                    sum+=(datetime.fromisoformat(result[i][0])-datetime.fromisoformat(result[i-1][0])).total_seconds() 
#  
            if result[-1][1]=='Перерыв' and datetime.fromisoformat(result[-1][0]).date!=datetime.now().date():
                eod = datetime.fromisoformat(result[-1][0])
                # eod.hour=18
                # eod.minute=0
                # eod.second=0
                eod = eod.replace(hour=18, minute=0, second=0)
                sum+=(eod - datetime.fromisoformat(result[-1][0])).total_seconds()
            minutes = int(int(sum)/60)
            if (sum<0):
                seconds = int(int(sum)%-60)*-1
            else:
                seconds = int(int(sum)%60)
            time_format = f"{minutes:02}:{seconds:02}"
            row[date[0]]=time_format
            
        return row
    
    def fetch_last_checkout(self,name:str):
        sql = f'''select timestamp, state
            from {name}
            where date(timestamp)=date('now')
            order by timestamp desc
            limit 1
            '''
        last_checkout = self.cursor.execute(sql).fetchone()
        sum_str = self.fetch_out_duration(name).split(':')
        sum = 3600 - timedelta(minutes=int(sum_str[0]), seconds=int(sum_str[1])).total_seconds()
        if (last_checkout and last_checkout[1]=='Перерыв'):
            sum += (datetime.now() - datetime.fromisoformat(last_checkout[0])).total_seconds()
        minutes, seconds = divmod(int(sum), 60)
        time_format = f"{minutes:02}:{seconds:02}"
        return time_format

    def insert_leave(self, name:str, time:str):
        sql = '''INSERT INTO leaves (timestamp, manager) VALUES (?, ?)'''
        try:
            self.cursor.execute(sql, (time, name))
            self.conn.commit()
        except sqlite3.OperationalError:
            print("something went wrong")

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS leaves (
                timestamp TIMESTAMP,
                manager VARCHAR(50),
                PRIMARY KEY (timestamp, manager)
            );''')
            self.cursor.execute(sql, (time, name))
            self.conn.commit()

    def drop_table(self, name:str):
        sql = f'DROP TABLE {name}'
        self.cursor.execute(sql)
        self.conn.commit()

    def rename_table(self, old_name:str, new_name:str):
        sql = f'ALTER TABLE {old_name} RENAME TO {new_name};'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print(f'Renamed {old_name} to {new_name}')
        except sqlite3.OperationalError:
            return
        
    def fetch_leaves(self, month:int, year:int=datetime.now().year):
        month = str(month).zfill(2)
        sql = f'''select strftime('%d', timestamp) as day, max(time(timestamp)), manager
                from leaves
                where strftime('%m', timestamp) = '{month}' and strftime('%Y', timestamp) = '{year}'
                group by day, manager'''
        try:
            return self.cursor.execute(sql).fetchall()
        except sqlite3.OperationalError:
            return
        
    def get_logs(self,name:str):
        date = datetime.now().isoformat()
            
        sql = f'''
                SELECT
                *
                FROM
                    {name}
                WHERE
                    date(timestamp) = date('{date}')
            '''
        
        return self.cursor.execute(sql).fetchall()

    def insert_busy(self, name:str, status:str):
        datetime.now().isoformat()
        sql = f'''insert into busy_status (timestamp, status, manager) values (?, ?, ?)'''
        try:
            self.cursor.execute(sql, (datetime.now().isoformat(), status, name))
            self.conn.commit()
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS busy_status (
                timestamp TIMESTAMP,
                status VARCHAR(50),
                manager VARCHAR(50),
                PRIMARY KEY (timestamp, manager)
            );''')
            self.cursor.execute(sql, (datetime.now().isoformat(), status, name))
            self.conn.commit()
    
    def fetch_busy(self, name:str):
        sql = f'''select status
                from busy_status
                where date(timestamp) = date('now') and manager = ?
                order by timestamp desc
                limit 1'''
        try:
            if self.cursor.execute(sql, (name,)).fetchone()[0] == "1":
                return True
            else:
                return False
            
        except TypeError:
            return False
        

    def fetch_leaves_timestamp(self, name:str):
        sql = f"""
SELECT timestamp
FROM leaves
WHERE manager = ?
ORDER BY timestamp DESC
LIMIT 1;
"""
        try:
            self.cursor.execute(sql, (name,))
            result = self.cursor.fetchone() 
            return result if result else None
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            return None