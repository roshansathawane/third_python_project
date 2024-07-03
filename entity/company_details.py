from sqlalchemy import Column, Integer, String, Date, Sequence
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class CompanyDetails(Base):
    __tablename__ = 'company_details'

 
    token_no = Column(Integer, Sequence('EXCEL_TOKEN_SEQ', start=1, increment=1), primary_key=True)
   
    excel_sr_no = Column(String(50), nullable=True)
   
    excel_name = Column(String(100), nullable=True)
    company_name = Column(String(100), nullable=True)
    website_url = Column(String(255), nullable=True)
    phone_no = Column(String(200), nullable=True)
    mobile_no = Column(String(200), nullable=True)
    address = Column(String(255), nullable=True)
    lastupdate = Column(Date, nullable=True)
    user_code = Column(String(20), nullable=True)
    email_id = Column(String(500), nullable=True)
    zaub_website = Column(String(500), nullable=True)
    zaub_phone_no = Column(String(500), nullable=True)
    zaub_email_id = Column(String(500), nullable=True)









# token_no = Column(String(50), nullable=True)
#     id = Column(Integer, primary_key=True)
#     excel_sr_no = Column(String(50), nullable=True)
#     # token_no = Column(String(50), nullable=True)
#     excel_name = Column(String(100), nullable=True)
#     company_name = Column(String(100), nullable=True)
#     website_url = Column(String(255), nullable=True)
#     phone_no = Column(String(200), nullable=True)
#     mobile_no = Column(String(200), nullable=True)
#     address = Column(String(255), nullable=True)
#     lastupdate = Column(Date, nullable=True)
#     user_code = Column(String(20), nullable=True)
#     email_id = Column(String(500), nullable=True)
#     zaub_website = Column(String(500), nullable=True)
#     zaub_phone_no = Column(String(500), nullable=True)
#     zaub_email_id = Column(String(500), nullable=True)
