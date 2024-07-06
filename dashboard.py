
from db_query_list import DBQueryList
from company_support import CompanySupport
# from entity.company_details import CompanyDetails
from dto.company_details_dto import CompanyDetailsDTO
import bcrypt


class Dashboard():
    def __init__(self):
        self.company_support = CompanySupport()
        self.db_query_list = DBQueryList()
     
    def userlogin(self, username, password ): 
        try:
            query = self.company_support.user_login()
            results = self.db_query_list.get_login_generic_list(query)
            
            print('results--------'+str(results))
            
            for result in results:
                user_name = result[0]
                pass_word = result[1]
            
            if user_name and pass_word: 
                if username == user_name and password == pass_word:
                    return 'Success'
                else:
                    return 'Fail'
            else:
                return 'No user found'   
        except Exception as e:
            print(f"Exception occurred in userlogin: {str(e)}")
            return 0 
    
    
   
        
    
    def get_company_details_count(self, filter_dto):
        try:
            count_query = self.company_support.get_company_data_count_query(filter_dto)
            list_count = self.db_query_list.get_row_count(count_query)
            return list_count if list_count > 0 else 0
        except Exception as e:
            print(f"Exception occurred in get_company_details_count: {str(e)}")
            return 0


    def get_company_details(self, filter_dto):
        try:
            query = self.company_support.get_company_data_query(filter_dto)
            return self.db_query_list.get_generic_list(CompanyDetailsDTO, query)
        except Exception as e:
            print(f"Exception occurred in get_company_details: {str(e)}")
            return []
        
        
        
    
    def get_company_details_data_count(self, filter_dto, company_token_no):
        list_count = 0
        try:
            count_query = self.company_support.get_company_details_data_count_query(filter_dto, company_token_no)
            list_count = self.db_query_list.get_row_count(count_query) 
            print('list_count----------'+str(list_count))
            return list_count if list_count > 0 else 0
        except Exception as e:
            print(f"Exception occurred in get_company_details_data_count: {str(e)}")
            return 0
    

    def get_company_details_data_count_grid(self, filter_dto, company_token_no):
        try:
            query = self.company_support.get_company_details_count_grid(filter_dto, company_token_no)
            return self.db_query_list.get_generic_list(CompanyDetailsDTO, query)

        except Exception as e:
            print(f"Exception occurred in get_company_details_data_count_grid: {str(e)}")
            return []
        
        
        
    def get_token_list(self):
        token_list = []
        try:
            query = self.company_support.get_token_List()
            print('query-------'+str(query))
            results = self.db_query_list.get_generic_list(CompanyDetailsDTO, query)
            token_list = [result.TOKEN_NO for result in results]
            return token_list
        except Exception as e:
            print(f"Error fetching token list: {str(e)}")
            return []
        
        
    def get_excel_list(self):
        excel_list= []
        try:
            query = self.company_support.get_excel_List()
            print('query-------'+str(query))
            results = self.db_query_list.get_generic_list(CompanyDetailsDTO, query)
            excel_list = [result.EXCEL_NAME for result in results]
            return excel_list
        except Exception as e:
            print(f"Error fetching excel_name list: {str(e)}")
            return []
        
        
    def get_incomp_excel_list(self):
        excel_list= []
        try:
            query = self.company_support.get_incomp_excel_List()
            print('query-------'+str(query))
            results = self.db_query_list.get_generic_list(CompanyDetailsDTO, query)
            excel_list = [(result.EXCEL_NAME, result.FLAG) for result in results]
            print('excel_list with flag:-----------', excel_list)
            return excel_list
        except Exception as e:
            print(f"Error fetching get_incomp_excel_list list: {str(e)}")
            return []
        
        
        
    def download_record_inDB(self, token):
        try:
            query, params = self.company_support.download_excelDetails_fromDB(token)
            db_query_list = DBQueryList()
            result = db_query_list.get_generic_list_download(query, params)
            return result
        except Exception as e:
            print(f"Exception occurred in download_record_inDB: {str(e)}")
            return f"Exception occurred in download_record_inDB: {str(e)}"
        
        
        
        
    