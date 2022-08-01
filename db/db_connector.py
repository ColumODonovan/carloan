import psycopg2
from configparser import ConfigParser
from psycopg2.errors import UndefinedTable


class DatabaseConnector():

    conn = None
    config = None
    
    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        self.config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return self.config


    def connect(self, config="database.ini"):
        try:
        
            print('Connecting to the PostgreSQL database...')
            params = self.config(config)
            self.conn = psycopg2.connect(**params)
            self.conn.autocommit = True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    

    def close_connection(self):
        print('Closing connection to the PostgreSQL database... ')
        self.conn.close()

    
    def create_table_csv(self, createQuery, copyQuery):
       
        cur = self.conn.cursor()
    
        print("Creating table...")
        cur.execute(createQuery)

        print("Copying data from CSV file to table...")
        cur.execute(copyQuery)
    
        print("Table created and populated")

    def create_table(self, createQuery):
        
        cur = self.conn.cursor()
        print("Creating table...")
        cur.execute(createQuery)
    
    def create_users(self):
        try:
            self.get_user("test")
        except UndefinedTable:
            self.create_table('''CREATE TABLE users (
                                    user_id bigint GENERATED ALWAYS AS IDENTITY,
                                    username  text,
                                    password text,
                                    CONSTRAINT user_id_pk PRIMARY KEY (user_id),
                                    CONSTRAINT unique_username UNIQUE (username));''')

    def insert_prediction(self, customer_id, prediction):
        self.conn.cursor().execute("INSERT INTO PREDICTIONS (customer_id, prediction) VALUES ({customer_id},{prediction});".format(customer_id=customer_id, prediction=prediction))        
    
    def insert_customer(self, customer):
        
        
        columns = ", ".join(list(customer.__dict__.keys()))
        values = ", ".join([str(val) for val in list(customer.__dict__.values())])  
        try:     
            self.conn.cursor().execute("INSERT INTO CUSTOMERS ({cols}) VALUES ({vals});".format(cols=columns, vals=values))
        except psycopg2.errors.UniqueViolation:
            pass 
    
    def insert_user(self, username, hashed_password):
        self.conn.cursor().execute("INSERT INTO USERS (username, password) VALUES ('{usr}','{password}');".format(usr=username, password=hashed_password))
    
    def get_user(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT username, password FROM USERS WHERE username='{usr}'".format(usr=username))        
        return cur.fetchone()
    
