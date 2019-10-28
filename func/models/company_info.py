class Company:
    name: str = ""
    cnpj: str = ""
    major_activity: str = ""
    sector: str = ""
    industry: str = ""
    web_site: str = ""
    cvm_code: str = ""

    def __init__(self, name = "", cnpj = "", major_activity = "", sector = "", industry = "", web_site = "", cvm_code = ""):
        self.name = name
        self.cnpj = cnpj
        self.major_activity = major_activity
        self.sector = sector
        self.industry = industry
        self.web_site = web_site
        self.cvm_code = cvm_code        
        pass
    pass