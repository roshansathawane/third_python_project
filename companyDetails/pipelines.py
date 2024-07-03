# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import cx_Oracle # type: ignore
class CompanydetailsPipeline:
 
    def get_connection():
        return cx_Oracle.connect(
        user="trainerp",
        password="trainerp",
        dsn="192.168.100.173:1521/ORA11G"  # DSN (Data Source Name) of your Oracle database
    )