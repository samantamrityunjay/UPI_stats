from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

class upi_ecosystem:
    def __init__(self, url):
        response = requests.get(url)
        html = response.text
        self.soup = BeautifulSoup(html, "html5lib")
        self.months = self.soup.find("select", attrs = {"id" : "yearDD", "class" : ["floatlabel","filled"]})
    
    def months_data(self):
        different_months = []
        monthwise_stat = {}
        for i in self.months.find_all("option"):
            different_months.append(i.text)
            
            tabular_data = {}
            tabular_data_names = ["remitter_bank", "beneficiary_bank", "upi_app_stat"]
            
            id = i['data-ddid']
            div_month = self.soup.find("div", attrs = {"class" : "hideDD", "id" : id})
            div_tables = div_month.find_all("div", attrs = {"class" : "table-responsive"})
            
                                        
            for table_index in range(2):
                rows = div_tables[table_index].table.tbody.find_all("tr")
                row_data = {"BankName":[],"TotalVolume":[],"Approved":[]}
                for row in rows:
                    columns = row.find_all("td")
                    row_data["BankName"].append(" ".join(columns[1].text.split()))
                    row_data["TotalVolume"].append(float(" ".join(columns[2].text.split())))
                    row_data["Approved"].append(float(" ".join(columns[3].text.split()).replace("%","")))
            
                tabular_data[tabular_data_names[table_index]] = row_data
            
            if len(div_tables)>2:
                rows = div_tables[2].table.tbody.find_all("tr")
                row_data = {"AppName":[],"TotalVolume":[],"TotalValue":[]}
                for row in rows:
                    columns = row.find_all("td")
                    row_data["AppName"].append(" ".join(columns[1].text.split()))
                    row_data["TotalVolume"].append(float("".join(" ".join(columns[-2].text.split()).split(","))))
                    row_data["TotalValue"].append(float("".join(" ".join(columns[-1].text.split()).split(","))))
            
                tabular_data[tabular_data_names[2]] = row_data
                
                                              
            monthwise_stat[self._month(i.text)] = tabular_data
            
            
        
        return monthwise_stat
    
    def _month(self,x):
        month_year = x.split()
        month = month_year[0][:3]
        year = month_year[1]
        return month + " " + year
                
    
    
                  
                  
        