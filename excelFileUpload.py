import pandas as pd
from db_query_list import DBQueryList
from excelFile_support import excelFileSupport
import random
from datetime import datetime
# from playwright.async_api import async_playwright


class ExcelFile:
    def __init__(self):
        self.current_token_number = 1000
        self.excel_support = excelFileSupport()
        self.db_query_list = DBQueryList()

   
    
    
    def read_excel_file(self, file_data, file_name):
        try:
            excelsheet_data = pd.read_excel(file_data)
            serial_no = 1
            token_number = self.excel_support.get_maxTokenNo()
            print('token_number------01------' + str(token_number))

            for _, row in excelsheet_data.iterrows():
                company_name = row.iloc[0]
                address = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else ''
                last_update = datetime.now()

                result_with_token = self.excel_support.insert_company_details(token_number, file_name, company_name,
                                                                           address, last_update, serial_no)
                serial_no += 1
                print('result_with_token-----------' + str(result_with_token))
            return result_with_token

        except Exception as e:
            print(f"Exception occurred in read_excel_file: {str(e)}")
    
    
  
     
     
                
    def get_company_fromDB(self, token):
        try:
            result = self.excel_support.get_companyName_fromDB(token)
            print('result---3--------'+str(result))
            return result 
        except Exception as e:
            print(f"Exception occured in get_company_fromDB : {str(e)}")   
            return (f"Exception occured in get_company_fromDB : {str(e)}")  
        
        

    def save_zaubaData_inDB(self, company_name, TokenNo, zaub_website, zaub_email, zaub_address, zaub_director_details):
        try:
            query = self.excel_support.set_zaubDetails_fromDB(company_name, TokenNo, zaub_website, zaub_email, zaub_address, zaub_director_details)
            result = self.db_query_list.update_query(query)
            
            return result 
        except Exception as e:
            print(f"Exception occured in get_company_fromDB : {str(e)}")   
            return (f"Exception occured in get_company_fromDB : {str(e)}")  
    
   
    
  
    def update_excelData_inDB(self, token, company_urls_str, emails, phones, company_name, zaub_website, zaub_email, zaub_address, zaub_director_details):
        try:
            print('zaub_website----1-----'+str(zaub_website))
            query, params = self.excel_support.set_excelDetails_fromDB(token, company_urls_str, emails, phones, company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            db_query_list = DBQueryList()
            result = db_query_list.update_query((query, params))
            return result
        except Exception as e:
            print(f"Exception occurred in update_excelData_inDB: {str(e)}")
            return f"Exception occurred in update_excelData_inDB: {str(e)}"
        
    
        
       
    
    def delete_record_inDB(self, token):
        try:
            query, params = self.excel_support.delete_excelDetails_fromDB(token)
            db_query_list = DBQueryList()
            result = db_query_list.delete_query(query, params)
            return result
        except Exception as e:
            print(f"Exception occurred in delete_record_inDB: {str(e)}")
            return f"Exception occurred in delete_record_inDB: {str(e)}"
        
        
        
    def get_max_token(self):
        try:
            token_number = self.excel_support.get_maxTokenNo()
            print('token_number------01------' + str(token_number))
            return token_number
        except Exception as e:
            print(f"Exception occurred in get_max_token: {str(e)}")
            return f"Exception occurred in get_max_token: {str(e)}"
        
        
        
        
    
        
        
        
   
    
    
    
        



