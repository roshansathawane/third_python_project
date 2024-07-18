
from db_query_list import DBQueryList
import pandas as pd
from datetime import datetime
import json


class excelFileSupport :
    def __init__(self):
        self.db_query_list = DBQueryList()
        
 
    def get_maxTokenNo(self):
        try:
            query = """
                SELECT MAX(TOKEN_NO) AS MAX_TOKEN_NO FROM company_details
            """
    
            cursor = self.db_query_list.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
    
            if result is not None and result[0] is not None:
                max_token_no = int(result[0])
                token_number = max_token_no + 1
            else:
                token_number = 101
                
            return token_number
            
        except Exception as e:
            print(f"Error get_maxTokenNo: {str(e)}")
            return None   
    
    
    
    def insert_company_details(self, token_number, file_name, company_name, address, last_update, serial_no):  
        query = """
            INSERT INTO company_details (TOKEN_NO, EXCEL_NAME, COMPANY_NAME, ADDRESS, USER_CODE, LASTUPDATE, EXCEL_SR_NO, FLAG)
            VALUES (:TOKEN, :EXCEL_NAME, :COMPANY_NAME, :ADDRESS, :USER_CODE, :LASTUPDATE, :EXCEL_SR_NO, :FLAG)
        """
        try:
            self.db_query_list.execute_query(query, {
                'TOKEN': token_number,
                'EXCEL_NAME': file_name,
                'COMPANY_NAME': company_name,
                'ADDRESS': address,
                'USER_CODE': 'LHS',
                'LASTUPDATE': last_update,
                'EXCEL_SR_NO': serial_no,
                'FLAG': 'N'
            })
            print(f"Successfully inserted data into the database: {str(query)}")
            return token_number
        except Exception as e:
            print(f"Error inserting company details: {str(e)}")
            return None
        

            
    def get_companyName_fromDB(self, token):
        query = """
            WITH company_cte AS (
                SELECT company_name, excel_sr_no, flag, COUNT(*) OVER () AS total_count
                FROM company_details
                WHERE token_no = :token
            )
            SELECT company_name, excel_sr_no, flag, total_count FROM company_cte
        """
        try:
            cursor = self.db_query_list.connection.cursor()
            cursor.execute(query, {'token': token})
            result = cursor.fetchall()
            cursor.close()
                       
            if result:
                company_details = [{'company_name': r[0], 'excel_sr_no': r[1], 'flag': r[2]} for r in result]
                count = result[0][3] 
            else:
                company_details = []
                count = 0
                
            return company_details, count
        except Exception as e:
            print(f"Error retrieving company names: {str(e)}")
            return [], 0
        
            
            
    def set_zaubDetails_fromDB(self, company_name, TokenNo, zaub_website, zaub_email, zaub_address, zaub_director_details):
        try:
            zaub_director_details_json = json.dumps(zaub_director_details)
            query = f"""
                UPDATE company_details
                SET ZAUB_URL = :WEBSITE_URL, zaub_address = :ADDRESS, ZAUB_EMAIL = :EMAIL, ZAUB_DIRECTOR_DETAILS = : ZAUB_DIRECTORS
                WHERE TOKEN_NO = :TOKEN AND COMPANY_NAME = :COMPANY_NAME
            """
            params = {
                'WEBSITE_URL': zaub_website,
                'EMAIL': zaub_email,
                'ADDRESS': zaub_address,
                'TOKEN': TokenNo,
                'COMPANY_NAME': company_name,
                'ZAUB_DIRECTORS': zaub_director_details_json
            }
            return query, params
        except Exception as e:
            print(f"Error in set_zaubDetails_fromDB: {str(e)}")
            return None, None
        
        
    
    
    
    def set_excelDetails_fromDB(self, token, company_urls_str, emails, phones, company_name, zaub_website, zaub_email, zaub_address, zaub_director_details):
        print(' inside set_excelDetails_fromDB')
        try: 
            zaub_director_details_json = json.dumps(zaub_director_details) if zaub_director_details else ''      
            query = """
                UPDATE company_details
                SET WEBSITE_URL = :WEBSITE_URL, PHONE_NO = :PHONE_NO, EMAIL = :EMAIL, ZAUB_URL = :ZAUB_URL, zaub_address = :zaub_address, ZAUB_EMAIL = :ZAUB_EMAIL, ZAUB_DIRECTOR_DETAILS = : ZAUB_DIRECTORS, FLAG = :FLAG
                WHERE TOKEN_NO = :TOKEN AND COMPANY_NAME = :COMPANY_NAME
            """
            params = {
                'WEBSITE_URL': company_urls_str,
                'EMAIL': emails,
                'PHONE_NO': phones,
                'TOKEN': token,
                'COMPANY_NAME': company_name,
                'ZAUB_URL': zaub_website,
                'zaub_address': zaub_address,
                'ZAUB_EMAIL': zaub_email,
                'ZAUB_DIRECTORS': zaub_director_details_json if zaub_director_details_json else '',
                'FLAG': 'P'
            }

            return query, params
        except Exception as e:
            print(f"Error in set_excelDetails_fromDB: {str(e)}")
            return None, None
        
        
        
   
    
    def delete_excelDetails_fromDB(self, token):
        try:
            query = """
                DELETE FROM company_details WHERE token_no = :token
            """
            params = {
                'token': token,
            }

            return query, params
        except Exception as e:
            print(f"Error in delete_excelDetails_fromDB: {str(e)}")
            return None, None
        
        
        
    