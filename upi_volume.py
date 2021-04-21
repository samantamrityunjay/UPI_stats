from bs4 import BeautifulSoup
import requests
import pandas as pd

class upi_product:
    def __init__(self, url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,"html5lib")
        table = soup.find("table", attrs = {"class":"table table-bordered"})
        header = table.thead
        body = table.tbody
        self.header_names = header.find_all("th")
        self.rows = body.find_all("tr")
                
    def data(self):
        data_dict = {" ".join(header.strong.text.split()):[] for header in self.header_names}
        key_list = list(data_dict.keys())
        
        for row in self.rows:
            columns = row.find_all('td')
            for i in range(len(key_list)):
                data_dict[key_list[i]].append("".join(" ".join(columns[i].text.split()).split(",")))
        
                
        df = pd.DataFrame(data_dict)
        convert_dict = {key_list[1]:int,
                       key_list[2]:float,
                       key_list[3]:float}
        df = df.astype(convert_dict)
        
        df['Month'] = df['Month'].apply(lambda x: self._month(x))
        df['Month'] = pd.to_datetime(df['Month'],format = "%b-%y")
        return df
    
        
    def _month(self, x):
        month_year = x.split("-")
        month = month_year[0][:3]
        year = month_year[1]
        return month+"-"+year
    
        
        
        
            