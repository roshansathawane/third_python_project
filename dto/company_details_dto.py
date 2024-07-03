           
class CompanyDetailsDTO:
    def __init__(self, startIndex='', endIndex='', excelName='', companyName='', phoneNo='', address='', token = '', fromDate= '', toDate= ''):
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.EXCEL_NAME = excelName
        self.COMPANY_NAME = companyName
        self.PHONE_NO = phoneNo
        self.ADDRESS = address
        self.TOKEN_NO = token
        self.FROM_DATE = fromDate
        self.TO_DATE = toDate
      
        
        

    def __repr__(self):
        return f"<CompanyDetailsDTO(token_no={self.TOKEN_NO}, fromDate={self.FROM_DATE}, toDate={self.TO_DATE})>"
        # return f"<CompanyDetailsDTO(token_no={self.TOKEN_NO})>"
    # def __repr__(self):
    #     return f"<CompanyDetailsDTO(startIndex={self.startIndex}, endIndex={self.endIndex}, excelName={self.excelName}, 
    # companyName={self.companyName}, phoneNo={self.phoneNo}, address={self.address}, fromDate={self.fromDate}, toDate={self.toDate})>"