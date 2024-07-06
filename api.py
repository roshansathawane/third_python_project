

import io
import json
from flask import Flask, request, jsonify, session, send_file, make_response, send_from_directory, Blueprint
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from util import Util
import pyautogui
from datetime import datetime



from companyDetails.spiders.emailtrack import EmailtrackSpider
from dashboard import Dashboard
from flask_cors import CORS
import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import cx_Oracle
import random
from io import BytesIO
import redis
import subprocess
import re

from entity.company_details import CompanyDetails
from dto.company_details_dto import CompanyDetailsDTO
from apiResponse import ApiResponse
from excelFileUpload import ExcelFile
import os
from bs4 import BeautifulSoup

angular_build_directory = 'S:/workspace/data_search/data_search_web/dataSearchWeb/dist'

app = Flask(__name__, static_folder=angular_build_directory)
CORS(app)

@app.route('/')
def serve_angular():
    
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)




# app = Flask(__name__)
# CORS(app)


def __init__(self, status_code, message, data):
        self.status_code = status_code
        self.message = message
        self.data = data
 
    
        
@app.route('/login', methods=['POST']) 
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
       
        dashboard_service = Dashboard()
        result = dashboard_service.userlogin(username, password)
        print('result-------'+str(result))
        return jsonify({ "message" : "success", "status": 200, "result": result})
          
    except Exception as e:
        app.logger.error(f"Error in login: {e}")
        return jsonify({'error': 'Failed to login'}), 500

    
 
        
@app.route('/upload', methods=['POST'])
def excelFile_Read():
    try:
        if 'fileInput' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['fileInput']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        file_name = str(file.filename)

        file_data = BytesIO(file.read())
        excel_service = ExcelFile()
        token_number = excel_service.read_excel_file(file_data, file_name)
       
    except Exception as e:
        app.logger.error(f"Error in excelFile_Read: {e}")
        return jsonify({'error': 'Failed to read excel file'}), 500

    return jsonify({ "message" : "success", "status": 200, "result": token_number})




@app.route('/getComapnyName/<token>', methods=['GET'])
def companyName_get_db(token):
    try:
        print('token--------' + str(token))
        excel_service = ExcelFile()
        company_details, count = excel_service.get_company_fromDB(token)
        
        if company_details:
            company_names = [detail['company_name'] for detail in company_details]
            serial_no = [detail['excel_sr_no'] for detail in company_details]
            flag = [detail['flag'] for detail in company_details]
            
            print('Company Names:-----6 ' + str(company_names))
            print('Serial Nos:---------6 ' + str(serial_no))
            print('Count:------6 ' + str(count))
            print('flag:------6 ' + str(flag))
            
            return jsonify({"message": "success", "status": 200, "company_names": company_names, "serial_no": serial_no, "count": count, "flag": flag})
        else:
            return jsonify({"message": "No companies found", "status": 404}), 404
     
    except Exception as e:
        app.logger.error(f"Error in companyName_get_db: {e}")
        return jsonify({'error': 'An error occurred'}), 500






@app.route('/searchCompany', methods=['POST'])
def search_company():
    try:
        data = request.get_json()
        company_name = data.get('companyName')
        token = str(data.get('token'))
        selected_details = data.get('selectedDetails', [])
        official_details = 'official_details' in selected_details
        zauba_details = 'zauba_details' in selected_details
               
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        zaub_result = None
        search_results = None
        
        if official_details and zauba_details:
            zaub_result = asyncio.run(zaub_search_with_playwright(company_name))           
            search_results = asyncio.run(search_with_playwright(company_name))

        elif official_details and not zauba_details:
            search_results = asyncio.run(search_with_playwright(company_name))

        elif not official_details and zauba_details:
            zaub_result = asyncio.run(zaub_search_with_playwright(company_name))

        
        zaub_website = None
        zaub_email = None
        zaub_address = None
        zaub_director_details = None
        
        if zaub_result:
            zaub_website = zaub_result.get('search_results')
            zaub_email = zaub_result.get('contact_text').split('Email ID:')[1].split('Website:')[0].strip() if 'Email ID:' in zaub_result.get('contact_text') else None
            zaub_address = zaub_result.get('contact_text').split('Address:')[1].split('\n')[0].strip() if 'Address:' in zaub_result.get('contact_text') else None
            zaub_director_details = zaub_result.get('row_data')

        
        if not search_results and zaub_result:
            company_urls_str =None
            result['emails'] = None
            result['phones'] = None
            excel_service = ExcelFile()
            excelFile_result = excel_service.update_excelData_inDB(token, company_urls_str, result['emails'], result['phones'], company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            return jsonify({"message": "success", "status": 200, "result": excelFile_result})
        
        if not search_results and not zaub_result:
            print('inside not search result--------------------------')
            zaub_website = None 
            zaub_email= None
            zaub_address = None
            zaub_director_details = None
            company_urls_str =None
            result = {
                'emails': None,
                'phones': None
            }
            excel_service = ExcelFile()
            excelFile_result = excel_service.update_excelData_inDB(token, company_urls_str, result['emails'], result['phones'], company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            return jsonify({'error': 'Failed to search company'}), 500
        
        playwright_result = search_results
        if search_results:
            com_urls = [url for url in search_results if url.endswith('.com/') or url.endswith('.com')]
            if not com_urls:
                in_urls = [url for url in search_results if url.endswith('.in/') or url.endswith('.in')]
                if not in_urls:
                    co_in_urls = [url for url in search_results if url.endswith('.co.in/') or url.endswith('.co.in')]
                    if not co_in_urls:
                        org_urls = [url for url in search_results if url.endswith('.org/') or url.endswith('.org')]
                        if not org_urls:
                            return jsonify({'error': 'No valid URLs found'}), 404
                        else:
                            urls_to_process = org_urls
                    else:
                        urls_to_process = co_in_urls
                else:
                    urls_to_process = in_urls
            else:
                urls_to_process = com_urls
                
                
            company_urls_str = ','.join(f'"{url}"' for url in urls_to_process)

            # company_urls_str =  urls_to_process


            process = subprocess.Popen(
                ['scrapy', 'crawl', 'emailtrack', '-a', f'company_urls=[{company_urls_str}]'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if stderr:
                print(f"Error running Scrapy spider: {stderr.decode('utf-8')}")

            result = {'emails': '', 'phones': ''}
            scrapy_data = stdout.decode('utf-8')

            emails_match = re.search(r"final_emails------------\[(.+?)\]", scrapy_data)
            if emails_match:
                emails_data = emails_match.group(1)
                emails = ',\n'.join(re.findall(r"'([^']+)'", emails_data))
                result['emails'] = emails

            phones_match = re.search(r"final_phones------------\[(.+?)\]", scrapy_data)
            if phones_match:
                phones_data = phones_match.group(1)
                phones = ',\n'.join(re.findall(r"'([^']+)'", phones_data))
                result['phones'] = phones

            excel_service = ExcelFile()
            if official_details and zauba_details:
                excelFile_result = excel_service.update_excelData_inDB(token, company_urls_str, result['emails'], result['phones'], company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            elif official_details and not zauba_details:
                zaub_website = None 
                zaub_email= None
                zaub_address = None
                zaub_director_details = None
                excelFile_result = excel_service.update_excelData_inDB(token, company_urls_str, result['emails'], result['phones'], company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            elif not official_details and zauba_details:
                company_urls_str =None
                result['emails'] = None
                result['phones'] = None
                excelFile_result = excel_service.update_excelData_inDB(token, company_urls_str, result['emails'], result['phones'], company_name, zaub_website, zaub_email, zaub_address, zaub_director_details)
            
            
            print('excelFile_result-------------'+excelFile_result)
        
        response_data = {
            'message': 'Search completed successfully',
            'status': 200,
            'Results': urls_to_process,
            'ScrapyResults': stdout.decode('utf-8'),
            # 'PlaywrightResults': search_results,
            'PlaywrightResults': playwright_result,
            'zaub_website': zaub_website,
            'zaub_email': zaub_email,
            'zaub_address': zaub_address,
            'zaub_director_details': zaub_director_details
        }

        print('cr_result---------', result)
        print('cr_result_emails---------', result['emails'])
        print('cr_result_phones---------', result['phones'])
        return jsonify(response_data)
    
    except Exception as e:
        app.logger.error(f"Error searching company: {e}")
        return jsonify({'error': 'Failed to search company'}), 500
    
    
    
    

# Serach single company date--------------------

@app.route('/searchsingleCompanyName', methods=['POST'])
def searchsingleCompanyName():
    try:
        filter_data = request.get_json()
        company_name = filter_data.get('companyName')
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        print('company_name--------' + str(company_name))
        zaub_result = None
        search_results = None
        
        zaub_result = asyncio.run(zaub_search_with_playwright(company_name))           
        search_results = asyncio.run(search_with_playwright(company_name))
        
        print('zaub_result-------------'+str(zaub_result))
        print('search_results-------------'+str(search_results))
 
        zaub_website = None
        zaub_email = None
        zaub_address = None
        zaub_director_details = None
        
        if zaub_result:
            zaub_website = zaub_result.get('search_results')
            zaub_email = zaub_result.get('contact_text').split('Email ID:')[1].split('Website:')[0].strip() if 'Email ID:' in zaub_result.get('contact_text') else None
            zaub_address = zaub_result.get('contact_text').split('Address:')[1].split('\n')[0].strip() if 'Address:' in zaub_result.get('contact_text') else None
            zaub_director_details = zaub_result.get('row_data')

           
        playwright_result = search_results
        if search_results:
            com_urls = [url for url in search_results if url.endswith('.com/') or url.endswith('.com')]
            if not com_urls:
                in_urls = [url for url in search_results if url.endswith('.in/') or url.endswith('.in')]
                if not in_urls:
                    co_in_urls = [url for url in search_results if url.endswith('.co.in/') or url.endswith('.co.in')]
                    if not co_in_urls:
                        org_urls = [url for url in search_results if url.endswith('.org/') or url.endswith('.org')]
                        if not org_urls:
                            return jsonify({'error': 'No valid URLs found'}), 404
                        else:
                            urls_to_process = org_urls
                    else:
                        urls_to_process = co_in_urls
                else:
                    urls_to_process = in_urls
            else:
                urls_to_process = com_urls
                
            company_urls_str = ','.join(f'"{url}"' for url in urls_to_process)
            # company_urls_str =  urls_to_process


            process = subprocess.Popen(
                ['scrapy', 'crawl', 'emailtrack', '-a', f'company_urls=[{company_urls_str}]'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if stderr:
                print(f"Error running Scrapy spider: {stderr.decode('utf-8')}")

            result = {'emails': '', 'phones': ''}
            scrapy_data = stdout.decode('utf-8')

            emails_match = re.search(r"final_emails------------\[(.+?)\]", scrapy_data)
            if emails_match:
                emails_data = emails_match.group(1)
                emails = ',\n'.join(re.findall(r"'([^']+)'", emails_data))
                result['emails'] = emails

            phones_match = re.search(r"final_phones------------\[(.+?)\]", scrapy_data)
            if phones_match:
                phones_data = phones_match.group(1)
                phones = ',\n'.join(re.findall(r"'([^']+)'", phones_data))
                result['phones'] = phones
                
            response_data = {
            'message': 'Search completed successfully',
            'status': 200,
            'Results': urls_to_process,
            'ScrapyResults': stdout.decode('utf-8'),
            # 'PlaywrightResults': search_results,
            'PlaywrightResults': playwright_result,
            'zaub_website': zaub_website,
            'zaub_email': zaub_email,
            'zaub_address': zaub_address,
            'zaub_director_details': zaub_director_details
        }

        print('cr_result---------', result)
        print('cr_result_emails---------', result['emails'])
        print('cr_result_phones---------', result['phones'])
        return jsonify(response_data)


    except Exception as e:
        app.logger.error(f"Error in searchsingleCompanyName: {e}")
        return jsonify({'error': 'Failed to process company name'}), 500
    
    


@app.route('/saveSingleCompanyData', methods=['POST'])
def save_single_company_data():
    filter_data = request.json
    company_details = filter_data.get('detailsToSave')  
    zaub_website = filter_data.get('zaub_website') 
    zaub_email = filter_data.get('zaub_email') 
    zaub_address = filter_data.get('zaub_address') 
    zaub_director_details = filter_data.get('zaub_director_details') 
     
    max_token = get_maxToken_for_singleCompany()
    print('max_token--------'+str(max_token))
    print('zaub_website--------'+str(zaub_website))
    print('zaub_email--------'+str(zaub_email))
    print('zaub_address--------'+str(zaub_address))
    print('zaub_director_details--------'+str(zaub_director_details))

    
   

    try:
        connection = cx_Oracle.connect(
            user="LHS_JAVA_DEV",
            password="LHS_JAVA_DEV",
            dsn="192.168.100.233:1521/orclpdb"
        )
        cursor = connection.cursor()

        for company in company_details.split('\n\n'):  
            company_info = company.split('\n')
          
            # print(f'Company Info: {company_info}')

            if len(company_info) < 5:
                print(f"Unexpected format for company details: {company}")
                continue

            company_name = ''
            website_url = ''
            emails = []
            phones = []

            for info in company_info:
                if info.startswith('Company Name:'):
                    company_name = info.split(': ')[1]
                    print('company_name-----------'+str(company_name))
                elif info.startswith('Website:'):
                    website_url = info.split(': ')[1]
                    print('website_url-----------'+str(website_url))
                elif info.startswith('Email:'):
                    emails.append(info.split(': ')[1].strip(','))
                elif info.startswith('Phone Number:'):
                    phones.append(info.split(': ')[1].strip(','))
                elif info and not info.startswith('Company') and not info.startswith('Website'):
                    if '@' in info:
                        emails.append(info.strip(','))
                    elif any(char.isdigit() for char in info):
                        phones.append(info.strip(','))
           
            if website_url == 'Website not found':
                print(f"Website not found for company: {company_name}, skipping database save.")
                continue    
               

            email_str = ', '.join(emails)
            phone_str = ', '.join(phones)

            last_update = datetime.now()
            # zaub_director_details_json = json.dumps(zaub_director_details) if zaub_director_details else ''     

            query = """
                INSERT INTO company_details (TOKEN_NO, COMPANY_NAME, WEBSITE_URL, EMAIL, PHONE_NO, USER_CODE, LASTUPDATE, ZAUB_URL, ZAUB_ADDRESS, ZAUB_EMAIL, ZAUB_DIRECTOR_DETAILS, FLAG)
                VALUES (:TOKEN, :COMPANY_NAME, :WEBSITE_URL, :EMAIL, :PHONE_NO, :USER_CODE, :LASTUPDATE, :ZAUB_URL, :ZAUB_ADDRESS, :ZAUB_EMAIL, :ZAUB_DIRECTOR_DETAILS, :FLAG)
            """
            print('query-------------'+str(query))
            cursor.execute(query, {
                'TOKEN': max_token,
                'COMPANY_NAME': company_name,
                'WEBSITE_URL': website_url,
                'EMAIL': email_str,
                'PHONE_NO': phone_str,
                'USER_CODE': 'LHS',
                'LASTUPDATE': last_update,
                'ZAUB_URL': zaub_website,
                'ZAUB_ADDRESS': zaub_address,
                'ZAUB_EMAIL': zaub_email ,
                'ZAUB_DIRECTOR_DETAILS' : zaub_director_details,  
                'FLAG' : 'p'
            })
            print(f'Company {company_name} details successfully saved in database with token: {max_token}')

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Data saved successfully', 'status': 200,  "result": max_token})
    except Exception as e:
        print("Error inserting data into database:", e)
        return jsonify({'error': 'Failed to save data'}), 500



    
    
def get_maxToken_for_singleCompany():
    try:   
        excel_service = ExcelFile()
        token_number = excel_service.get_max_token()
        print('token_number----------'+str(token_number))
        
        return token_number
        
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"status": "error", "count": 0}), 500
    


# end single company process
# -------------------------------------------------

@app.route('/getcompanyDashFiltTableCount', methods=['POST'])
def get_company_data_count():
    try:
        filter_data = request.json
        filter_data = request.json
        print('Received filter_data:', filter_data)
        token = filter_data.get('token', None)
        print('Received token:', token)
        
        
        dashboard_service = Dashboard()
        count = dashboard_service.get_company_details_count(filter_data)
        
        print(f"Inside getcompanyDashFiltTableCount count: {count}")
        return jsonify({ "message" : "success", "status": 200, "result": count})
        
        
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"status": "error", "count": 0}), 500





@app.route('/getcomapnyDataGridDetails', methods=['POST'])
def get_company_data_grid_details():
    print('inside get_company_data_grid_details method')

    try:
        filter_data = request.json
        filter_data = {
            'startIndex': filter_data.get('startindex', ''),
            'endIndex': filter_data.get('endIndex', ''),
            'excelName': filter_data.get('EXCEL_NAME', ''),
            'companyName': filter_data.get('COMPANY_NAME', ''),
            'phoneNo': filter_data.get('PHONE_NO', ''),
            'address': filter_data.get('address', ''),
            'token': filter_data.get('token', '')  
        }
        
        filter_dto = CompanyDetailsDTO(**filter_data)
        print("Inside getcompanyDataGridDetails")

        dashboard_service = Dashboard()
        company_details = dashboard_service.get_company_details(filter_dto) 
        
        print('company_details-----55------'+str(company_details))

        print(f"Inside getcompanyDataGridDetails count: {len(company_details)}")
        return jsonify({"message": "success", "status": 200,  "result": [vars(obj) for obj in company_details]})
        

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"status": "error", "company_details": []}), 500



@app.route('/getcompanyDetailsDashFiltTableCount/<companyTokenNo>', methods=['POST'])
def get_company_detail_data_count(companyTokenNo):
    try:
        print('companyTokenNo:', companyTokenNo)
        filter_data = request.json
        filter_data = {
            'startIndex': filter_data.get('startindex', ''),
            'endIndex': filter_data.get('endIndex', ''),
            'excelName': filter_data.get('EXCEL_NAME', ''),
            'companyName': filter_data.get('COMPANY_NAME', ''),
            'phoneNo': filter_data.get('PHONE_NO', ''),
            'address': filter_data.get('address', '')
        }
        
        filter_dto = CompanyDetailsDTO(**filter_data)
        dashboard_service = Dashboard()
        count = dashboard_service.get_company_details_data_count(filter_dto, str(companyTokenNo))   
        print(f"Inside getcompanyDetailsDashFiltTableCount count: {count}")
        return jsonify({"message": "success", "status": 200, "result": str(count)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@app.route('/getcomapnyDetailsDataGrid/<companyTokenNo>', methods=['POST'])
def getcomapnyDetailsDataGrid(companyTokenNo):
    try:
        filter_data = request.json
               
        filter_data = {
            'startIndex': filter_data.get('startindex', ''),
            'endIndex': filter_data.get('endIndex', ''),
            'excelName': filter_data.get('EXCEL_NAME', ''),
            'companyName': filter_data.get('COMPANY_NAME', ''),
            'phoneNo': filter_data.get('PHONE_NO', ''),
            'address': filter_data.get('address', ''),
            'fromDate': filter_data.get('From_date', ''),
            'toDate': filter_data.get('to_date', ''),
            
        }
        
        filter_dto = CompanyDetailsDTO(**filter_data)
        dashboard_service = Dashboard()
        company_details = dashboard_service.get_company_details_data_count_grid(filter_dto, str(companyTokenNo)) 
        print('company_details----66--------'+str(company_details))
        return jsonify({"message": "success", "status": 200, "result": [vars(obj) for obj in company_details]})
        
    except Exception as e:
        return jsonify({'error': str(e)}) , 500   



@app.route('/get_tokenlist', methods=['GET'])
def get_tokenlist():
    try:
        dashboard_service = Dashboard()
        token_list = dashboard_service.get_token_list()
        return jsonify({"message": "success", "status": 200, "result": token_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/get_excellist', methods=['GET'])
def get_excellist():
    try:
        dashboard_service = Dashboard()
        excel_list = dashboard_service.get_excel_list()
        return jsonify({"message": "success", "status": 200, "result": excel_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
@app.route('/get_incomp_excellist', methods=['GET'])
def get_incomp_excellist():
    try:
        dashboard_service = Dashboard()
        incomp_excel_list = dashboard_service.get_incomp_excel_list()
        return jsonify({"message": "success", "status": 200, "result": incomp_excel_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    
@app.route('/get_zaubDetails', methods=['POST'])
def get_zaubDetails():
    try:
        print('inside get_zaubDetails method')
        data = request.get_json()
        company_name = data.get('companyName')
        TokenNo = data.get('companyTokenNo')
                
        result_data  = asyncio.run(zaub_search_with_playwright(company_name))
        print('result_data----1---'+str(result_data))
        
        
        
        if result_data:
            print('Search Results:', result_data['search_results'])
            print('Email ID:----------', result_data['contact_text'].split('Email ID:')[1].split('Website:')[0].strip())
            print('Address:-----------', result_data['contact_text'].split('Address:')[1].split('\n')[0].strip())

            print('row_data---------', result_data['row_data'])

            for row in result_data['row_data']:
                print('DIN Value:-----', row['din_value'])
                print('Name:-----', row['name_value'])
                print('Designation-----:', row['designation_value'])
                
        
        else:
            print('No data found.')
        
        
        return jsonify({"message": "success", "status": 200, "result": {"result_data": result_data}})       
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/save_zaubDetails', methods=['POST'])
def save_zaubDetails():
    try:
        print('inside save_zaubDetails method')
        data = request.get_json()
        TokenNo = data.get('companyTokenNo')
        company_name = data.get('company_name')
        websiteUrl = data.get('websiteUrl')
        email = data.get('email')
        address = data.get('address')
        
        zaub_result_json = data.get('zaub_result')
        zaub_result = json.loads(zaub_result_json)

        if zaub_result:
            zaub_website = zaub_result['search_results']
            zaub_email = zaub_result['contact_text'].split('Email ID:')[1].split('Website:')[0].strip()
            zaub_address = zaub_result['contact_text'].split('Address:')[1].split('\n')[0].strip()
            zaub_director_details = zaub_result['row_data']
            print('zaub_director_details---------'+str(zaub_director_details))

            print('Row Data:')
            for row in zaub_director_details:
                print('DIN Value:', row['din_value'])
                print('Name:', row['name_value'])
                print('Designation:', row['designation_value'])

            excel_service = ExcelFile()
            zauba_result = excel_service.save_zaubaData_inDB(company_name, TokenNo, zaub_website, zaub_email, zaub_address, zaub_director_details)
            print('zaub_details:', zauba_result)
        return jsonify({"message": "success", "status": 200})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

    
     
   
@app.route('/delete_record/<token>', methods=['GET'])  
def delete_record(token):    
    try:
        print('token-------delete--------'+token)               
        excel_service = ExcelFile()
        delete_record = excel_service.delete_record_inDB(token)
        print('delete_record---------------'+str(delete_record))
        return jsonify({"message": "success", "status": 200})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    


@app.route('/download_excel/<token>', methods=['GET'])
def download_excel(token):
    try:
        print(f"Received request for token: {token}")
        dashboard_service = Dashboard()
        download_excel_record = dashboard_service.download_record_inDB(token)
          
        if download_excel_record:
            df = pd.DataFrame(download_excel_record)
            print("DataFrame created successfully")

            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1')

            workbook = writer.book
            worksheet = workbook.get_worksheet_by_name('Sheet1')
            
            column_width_cm = 1
            column_width_points = column_width_cm * 28.35
            for col_num, value in enumerate(df.columns.values):
                worksheet.set_column(col_num, col_num, column_width_points)
                
                
            center_format = workbook.add_format({'align': 'center'})
            worksheet.set_column('A:B', None, center_format)

            writer.close() 
            output.seek(0)
            print("Excel file created successfully")

            response = send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='company_data.xlsx'
            )
            print("Response created successfully")
            return response
           
           
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500





async def search_with_playwright(company_name):
    
    try:
        print('company_name----search_with_playwright------------'+company_name)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(f'https://www.google.com/search?q={company_name}')

            search_results = await page.evaluate(
                 """() => {
                 const links = Array.from(document.querySelectorAll('div.tF2Cxc a'));
                 const officialWebsites = {};
                 for (const link of links) {
                     const href = link.getAttribute('href');
                     if (href && !href.startsWith('/search') &&
                         !href.includes("facebook.com") &&
                         !href.includes("indiamart.com") &&
                         !href.includes("justdial.com") &&
                         !href.includes("indiafilings.com") &&
                         !href.includes("amazon.in") &&
                         !href.includes("instagram.com") &&
                         !href.includes("tradeindia.com") &&
                         !href.includes("linkedin.com") &&
                         !href.includes("zaubacorp.com") &&
                         !href.includes("wikipedia.org") &&
                         !href.includes("indiainfoline.com") &&
                         (href.endsWith('.com') || href.endsWith('.com/') || href.endsWith('.in') || href.endsWith('.in/') || href.endsWith('.org') || href.endsWith('.org/'))){
                             const domain = new URL(href).hostname.replace('www.', '');
                             if (!(domain in officialWebsites)) {
                                 officialWebsites[domain] = href;
                             }
                     }
                 }
                 return Object.values(officialWebsites);
             }"""
            )

            await browser.close()
            
            return search_results

    except Exception as e:
        print('Error in search_with_playwright:', str(e))
        return []
    
    
    




async def zaub_search_with_playwright(company_name):
    try:
        print(f'company_name----search_with_playwright------------{company_name}')
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            pyautogui.hotkey('win', 'down')

            query = f'{company_name} zauba'
            await page.goto(f'https://www.google.com/search?q={query}')
            
            await page.wait_for_selector('div.tF2Cxc a')

            search_results = await page.evaluate(
                """() => {
                    const links = Array.from(document.querySelectorAll('div.tF2Cxc a'));
                    for (const link of links) {
                        const href = link.getAttribute('href');
                        if (href && href.includes("zaubacorp.com")) {
                            return href; // Return the first Zauba link found
                        }
                    }
                    return null; // No Zauba link found
                }"""
            )

            print('search_results--------------' + search_results)
            if search_results:
                await page.goto(search_results)
                await page.wait_for_selector('body') 
                await page.wait_for_timeout(5000)  
                body_text = await page.evaluate('document.body.innerText')
                rows = await page.query_selector_all('#block-system-main > div.contaier > div.container.information > div.col-lg-12.col-md-12.col-sm-12.col-xs-12 > table > tbody > tr')

                row_data = []

                for row in rows:
                    td_elements = await row.query_selector_all('td')
                    din_value = None
                    name_value = None
                    designation_value = None
                    for td in td_elements:
                        td_text = await td.text_content()
                        if re.match(r'^\d{8}$', td_text.strip()):
                            din_value = td_text.strip()
                        elif 'Director' in td_text.strip():
                            designation_value = td_text.strip()
                        elif name_value is None and not re.match(r'^\d{8}$', td_text.strip()) and 'Director' not in td_text.strip():
                            name_value = td_text.strip()

                    if din_value and name_value and designation_value:
                        print(f'TD Text:---------- {din_value}')
                        print(f'TD Text:---------- {name_value}')
                        print(f'TD Text:---------- {designation_value}')

                        row_data.append({
                            'din_value': din_value,
                            'name_value': name_value,
                            'designation_value': designation_value
                        })

                contact_details_content_elements = await page.query_selector_all('#block-system-main > div.contaier > div.container.information > div:nth-child(15) > div > div:nth-child(1)')
                contact_text = ''
                for contact_content in contact_details_content_elements:
                    contact_text += await contact_content.text_content() + '\n'

                await browser.close()

                # Combine all data into a single variable
                result_data = {
                    'search_results': search_results,
                    'contact_text': contact_text,
                    'row_data': row_data
                }

                return result_data

            await browser.close()
            print('No ZaubaCorp link found.')
            return None

    except Exception as e:
        print(f'Error in zaub_search_with_playwright: {str(e)}')
        return None




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)