
import cx_Oracle

class DBQueryList:
    def __init__(self):
        self.connection = self.get_db_connection()

 
    def get_db_connection(self):
        try:
            connection = cx_Oracle.connect(
                user="LHS_JAVA_DEV",
                password="LHS_JAVA_DEV",
                dsn="192.168.100.233:1521/orclpdb"
            )
            return connection
        except Exception as e:
            print(f"Error connecting to the database: {str(e)}")
            return None
        
           
    
    def get_row_count(self, query):
        if not self.connection:
            print("No database connection available.")
            return 0

        count = 0
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    count = result[0]
        except Exception as e:
            print(f"Exception occurred in get_row_count: {str(e)}")
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None
        return count
    
    
    def get_generic_list(self, object_type, query):
        list_data = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                for row in cursor.fetchall():
                    result_data = object_type()
                    for idx, col in enumerate(columns):
                        value = row[idx]
                        setattr(result_data, col, value)
                    list_data.append(result_data)
        except Exception as e:
            print(f"Exception occurred in get_generic_list: {str(e)}")
        return list_data
    
    
    
    
    
    
      
    
    def execute_query(self, query, params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return "Update successful"
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            
    
            
            
    def update_query(self, query_params):
        query, params = query_params
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return "Update successful"
        except Exception as e:
            print(f"Exception occurred in execute_query: {str(e)}")
            return f"Exception occurred in execute_query: {str(e)}"
        
        
    def update_query1(self, query, params):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return "Update successful"
        except Exception as e:
            print(f"Exception occurred in execute_query: {str(e)}")
            return f"Exception occurred in execute_query: {str(e)}"
        
        
    
    
 

    def delete_query(self, query, params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return "Success"
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return f"Error executing query: {str(e)}"
        
        
        
   
    
    def get_generic_list_download(self, query, params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            cursor.close()
            print(f"Query executed successfully, fetched rows: {rows}")
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None
        
        
    def get_login_generic_list(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return None