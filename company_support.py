from util import Util
# from dashboard import Dashboard
from entity.company_details import CompanyDetails
from dto.company_details_dto import CompanyDetailsDTO
from db_query_list import DBQueryList

class CompanySupport:
    
    def user_login(self):
        query = """
            select user_code, password from user_mast1
        """
        return query
    
    
    
    @staticmethod       
    def get_company_data_count_query(filter_dto):
        query = """
            SELECT count(*) from (
                SELECT rownum slno,
                    id,
                    excel_sr_no,
                    token_no,
                    excel_name,
                    company_name,
                    website_url,
                    phone_no,
                    address,
                    lastupdate,
                    email,
                    user_code,
                    zaub_url,
                    zaub_address,
                    zaub_email,
                    flag

                FROM (
                    SELECT
                        ROW_NUMBER() OVER(PARTITION BY t.token_no ORDER BY t.id ) AS slno,
                        t.id,
                        t.excel_sr_no,
                        t.token_no,
                        t.excel_name,
                        t.company_name,
                        t.website_url,
                        t.phone_no,
                        t.address,
                        t.lastupdate,
                        t.email,
                        t.user_code,
                        t.zaub_url,
                        t.zaub_address,
                        t.zaub_email,
                        t.flag

                    FROM company_details t
                    WHERE 1=1
        """       
            
        if not Util.isnull(filter_dto.get("EXCEL_NAME")):
            query += f" AND LOWER(t.excel_name) LIKE LOWER('%{filter_dto['EXCEL_NAME']}%')"
            
        
        if not Util.isnull(filter_dto.get("token")):
           query += f" AND LOWER(t.token_no) LIKE LOWER('%{filter_dto['token']}%')"

        query += ") WHERE slno = 1) ORDER BY slno"
        print(f"Data Query----01------: {query}")
        return query
        
        
    
    def get_company_data_query(self, filter_dto):
        query = """
            select * from (
                SELECT  ROW_NUMBER() OVER(ORDER BY LASTUPDATE desc) AS slno,
                    id,
                    excel_sr_no,
                    token_no,
                    excel_name,
                    company_name,
                    website_url,
                    phone_no,
                    address,
                    lastupdate,
                    email,
                    user_code,
                    zaub_url,
                    zaub_address,
                    zaub_email,
                    flag
                
                FROM (
                    SELECT 
                        ROW_NUMBER() OVER(PARTITION BY t.token_no ORDER BY t.id ) AS slno,
                        t.id,
                        t.excel_sr_no,
                        t.token_no,
                        t.excel_name,
                        t.company_name,
                        t.website_url,
                        t.phone_no,
                        t.address,
                        t.lastupdate,
                        t.email,
                        t.user_code,
                        t.zaub_url,
                        t.zaub_address,
                        t.zaub_email,
                        t.flag
                    
                        
                    FROM company_details t
                    WHERE 1=1
        """

        if not Util.isnull(filter_dto.EXCEL_NAME):
            query += f" AND LOWER(t.excel_name) LIKE LOWER('%{filter_dto.EXCEL_NAME}%')"
            
        
        if not Util.isnull(filter_dto.TOKEN_NO):
            query += f" AND LOWER(t.token_no) LIKE LOWER('%{filter_dto.TOKEN_NO}%')"           

        query += ") WHERE slno = 1)\n" + \
            f"where slno between {filter_dto.startIndex} AND {filter_dto.endIndex}\n" + \
            "ORDER BY slno "
        print("Data Query...02...", query)
        return query
    
    
    


    def get_company_details_data_count_query(self, filter_dto, company_token_no):
        print('company_token_no-------------'+company_token_no)
        query = """
            SELECT count(*)
                FROM (SELECT ROW_NUMBER() OVER(ORDER BY t.LASTUPDATE DESC) AS slno,
                   t.id,
                   t.excel_sr_no,
                   t.token_no,
                   t.excel_name,
                   t.company_name,
                   t.website_url,
                   t.phone_no,
                   t.address,
                   t.lastupdate,
                   t.email,
                   t.user_code,
                   t.zaub_url,
                   t.zaub_address,
                   t.zaub_email,
                   t.flag
                
                FROM company_details t
                WHERE 1=1 AND t.Token_No = '%s'
        """ %company_token_no

        if not Util.isnull(filter_dto.EXCEL_NAME):
            query += f" AND LOWER(t.excel_name) LIKE LOWER('%{filter_dto.EXCEL_NAME}%')"

        if not Util.isnull(filter_dto.COMPANY_NAME):
            query += f" AND LOWER(t.company_name) LIKE LOWER('%{filter_dto.COMPANY_NAME}%')"

        if not Util.isnull(filter_dto.PHONE_NO):
            query += f" AND t.phone_no LIKE '%{filter_dto.PHONE_NO}%'"

        if not Util.isnull(filter_dto.ADDRESS):
            query += f" AND t.address LIKE '%{filter_dto.ADDRESS}%'"

        query += ") ORDER BY slno"

        print("Data Query....03..", query)
        return query
    
    
    
    
   
    
    def get_company_details_count_grid(self, filter_dto, company_token_no):
        query = """
            SELECT *
                FROM (SELECT ROW_NUMBER() OVER(ORDER BY t.LASTUPDATE DESC) AS slno,
                   t.id,
                   t.excel_sr_no,
                   t.token_no,
                   t.excel_name,
                   t.company_name,
                   t.website_url,
                   t.phone_no,
                   t.address,
                   t.lastupdate,
                   t.email,
                   t.user_code,
                   t.zaub_url,
                   t.zaub_address,
                   t.zaub_email,
                   t.flag,
                   t.zaub_director_details
                 
                FROM company_details t
                WHERE 1=1 AND t.Token_No='{0}'
        """.format(company_token_no)

        # if filter_dto.EXCEL_NAME:
        #     query += f" AND LOWER(t.excel_name) LIKE LOWER('%{filter_dto.EXCEL_NAME}%')"

        if filter_dto.COMPANY_NAME:
            query += f" AND LOWER(t.company_name) LIKE LOWER('%{filter_dto.COMPANY_NAME}%')"

        if filter_dto.PHONE_NO:
            query += f" AND t.phone_no LIKE '%{filter_dto.PHONE_NO}%'"

        if filter_dto.ADDRESS:
            query += f" AND t.address LIKE '%{filter_dto.ADDRESS}%'"
            
        if filter_dto.FROM_DATE:
            query += f" AND t.lastupdate >= TO_DATE('{filter_dto.FROM_DATE}', 'YYYY-MM-DD')"
            
        if filter_dto.TO_DATE:
            query += f" AND t.lastupdate <= TO_DATE('{filter_dto.TO_DATE}', 'YYYY-MM-DD')"
            

        query += ") WHERE slno BETWEEN {0} AND {1}\nORDER BY slno".format(filter_dto.startIndex, filter_dto.endIndex)
       

        print("Data Query...04...", query)
        return query
    
    
    
    
    
    def get_token_List(self):
        query= """  
            select DISTINCT  token_no from company_details
        """
        return query
    

    def get_excel_List(self):
        query= """  
            select DISTINCT token_no, excel_name from company_details
        """
        return query
    
    def get_incomp_excel_List(self):
        query= """  
            select DISTINCT token_no, excel_name, flag from company_details where flag = 'N'
        """
        return query
    
    
    

    def download_excelDetails_fromDB(self, token):
        try:
            print(f"Received token: {token}")
            query = """
                SELECT ROW_NUMBER() OVER(ORDER BY t.token_no DESC) AS srNo,
                       t.token_no,
                       t.excel_name,
                       t.company_name,
                       t.website_url,
                       t.phone_no,
                       t.address,
                       t.email,
                       t.zaub_url,
                       t.zaub_address,
                       t.zaub_email,
                       t.zaub_director_details
                FROM company_details t
                WHERE t.token_no = :token
            """
            params = {'token': token}
            print(f"Generated query: {query}")
            print(f"Query parameters: {params}")
            return query, params
        except Exception as e:
            print(f"Error in download_excelDetails_fromDB: {str(e)}")
            return None, None