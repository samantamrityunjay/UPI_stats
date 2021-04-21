
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
from datetime import datetime

from upi_volume import upi_product
from upi_ecosystem import upi_ecosystem
url = "https://www.npci.org.in/what-we-do/upi/product-statistics"
url_ecosystem = "https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics"


st.title("UPI statistics")

@st.cache
def get_data(url_product,url_ecosystem):
    data_upi_product = upi_product(url)
    data_df = data_upi_product.data()
    
    upi_apps = upi_ecosystem(url_ecosystem)
    whole_stat = upi_apps.months_data()
    
    return data_df,whole_stat

data_df,whole_stat = get_data(url, url_ecosystem)

@st.cache
def get_upi_app_data(whole_stat):
    months = [datetime.strptime(x, '%b %Y') for x in whole_stat.keys() if "upi_app_stat" in whole_stat[x].keys()]
    
    all_upi_apps = list(set([app for x in whole_stat.keys() if "upi_app_stat" in whole_stat[x].keys() for app in whole_stat[x]["upi_app_stat"]["AppName"]]))
    
    upi_app_monthly_value = {}
    upi_app_monthly_volume = {}
    for app in all_upi_apps:
        upi_app_monthly_value[app] = [whole_stat[key]["upi_app_stat"]["TotalValue"][whole_stat[key]["upi_app_stat"]["AppName"].index(app)] if app in whole_stat[key]["upi_app_stat"]["AppName"] else 0 for key in whole_stat.keys() if "upi_app_stat" in whole_stat[key].keys()]
        
        upi_app_monthly_volume[app] = [whole_stat[key]["upi_app_stat"]["TotalVolume"][whole_stat[key]["upi_app_stat"]["AppName"].index(app)] if app in whole_stat[key]["upi_app_stat"]["AppName"] else 0 for key in whole_stat.keys() if "upi_app_stat" in whole_stat[key].keys()]
        
    return months, all_upi_apps, upi_app_monthly_value, upi_app_monthly_volume

upi_months, all_upi_apps, upi_app_monthly_value, upi_app_monthly_volume = get_upi_app_data(whole_stat)

@st.cache
def get_remit_bank_data(whole_stat):
    months = [datetime.strptime(x, '%b %Y') for x in whole_stat.keys()]
    
    all_remit_banks = list(set([bank for month in whole_stat.keys() for bank in whole_stat[month]['remitter_bank']["BankName"]]))
    
    remit_bank_monthly_volume = {}
    remit_bank_monthly_failure = {}
    for bank in all_remit_banks:
        remit_bank_monthly_volume[bank] = [whole_stat[key]["remitter_bank"]["TotalVolume"][whole_stat[key]["remitter_bank"]["BankName"].index(bank)] if bank in whole_stat[key]["remitter_bank"]["BankName"] else 0 for key in whole_stat.keys()]
        
        remit_bank_monthly_failure[bank] = [100 - whole_stat[key]["remitter_bank"]["Approved"][whole_stat[key]["remitter_bank"]["BankName"].index(bank)] if bank in whole_stat[key]["remitter_bank"]["BankName"] else 0 for key in whole_stat.keys()]
        
    return months, all_remit_banks, remit_bank_monthly_volume, remit_bank_monthly_failure

remit_months, all_remit_banks, remit_bank_monthly_volume, remit_bank_monthly_failure = get_remit_bank_data(whole_stat)


@st.cache
def get_benefit_bank_data(whole_stat):
    months = [datetime.strptime(x, '%b %Y') for x in whole_stat.keys()]
    
    all_benefit_banks = list(set([bank for month in whole_stat.keys() for bank in whole_stat[month]['beneficiary_bank']["BankName"]]))
    
    benefit_bank_monthly_volume = {}
    benefit_bank_monthly_failure = {}
    for bank in all_benefit_banks:
        benefit_bank_monthly_volume[bank] = [whole_stat[key]["beneficiary_bank"]["TotalVolume"][whole_stat[key]["beneficiary_bank"]["BankName"].index(bank)] if bank in whole_stat[key]["beneficiary_bank"]["BankName"] else 0 for key in whole_stat.keys()]
        
        benefit_bank_monthly_failure[bank] = [100 - whole_stat[key]["beneficiary_bank"]["Approved"][whole_stat[key]["beneficiary_bank"]["BankName"].index(bank)] if bank in whole_stat[key]["beneficiary_bank"]["BankName"] else 0 for key in whole_stat.keys()]
        
    return months, all_benefit_banks, benefit_bank_monthly_volume, benefit_bank_monthly_failure

benefit_months, all_benefit_banks, benefit_bank_monthly_volume, benefit_bank_monthly_failure = get_benefit_bank_data(whole_stat)   
       
    

type_statistic = st.sidebar.selectbox("Type of statistics",("Overall UPI product", "UPI Ecosystem"))

if type_statistic == "Overall UPI product":
    st.header("Overall UPI product statistics")
            
    fig,ax = plt.subplots(figsize = (16,9))
    ax.bar(data_df.iloc[:,0], data_df.iloc[:,1], color = 'r')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval= 2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.xticks(rotation = 90)
    plt.title("No. of banks live on UPI", fontsize= 20)
    plt.ylabel("No. of banks", fontsize= 14)
    plt.xlabel("Year", fontsize= 14)   
    st.pyplot(fig)
    
    fig,ax = plt.subplots(figsize = (16,9))
    s = [0.5*x for x in data_df.iloc[:,2]]
    ax.scatter(data_df.iloc[:,0], data_df.iloc[:,2], s = s, color = 'r')
    ax.set_xlabel("year",fontsize=16)
    ax.set_ylabel("Volume (in Mn)",color="red",fontsize=16)
    
    ax2=ax.twinx()
    ax2.plot(data_df.iloc[:,0], data_df.iloc[:,3], color = 'b')
    ax2.set_xlabel("year",fontsize=16)
    ax2.set_ylabel("Value (in Cr)",color="blue",fontsize=16)
    
    plt.title("Volume and value of transactions on UPI", fontsize=20)
    
    st.pyplot(fig)
    
    st.write(data_df)
    
else:
    upi_ecosystem_type = st.sidebar.selectbox("Type of ecosystem", ["UPI Apps", "Remitter Banks", "Beneficiary Banks"])    
    
    if upi_ecosystem_type == "UPI Apps":
        st.header("UPI apps statistics")  
        selected_apps = st.multiselect("Select UPI App", all_upi_apps, default = ["PhonePe", "Google Pay"])
        
        fig = plt.figure()
        for app in selected_apps:
            plt.plot(upi_months, upi_app_monthly_value[app], label = app)
        plt.title("UPI value", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("Value (in Cr)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
        fig = plt.figure()
        for app in selected_apps:
            plt.plot(upi_months, upi_app_monthly_volume[app], label = app)
        plt.title("UPI volume", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("Volume (in Mn)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
        
    elif upi_ecosystem_type == "Remitter Banks":
        
        st.header("Remitter Bank statistics")  
        selected_banks = st.multiselect("Select Bank", all_remit_banks, default = all_remit_banks[:3])
        
        fig = plt.figure()
        for bank in selected_banks:
            plt.plot(remit_months, remit_bank_monthly_volume[bank], label = bank)
        plt.title("Remit volume", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("Volume (in Mn)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
        fig = plt.figure()
        for bank in selected_banks:
            plt.plot(remit_months, remit_bank_monthly_failure[bank], label = bank)
        plt.title("Remit failures", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("failure (in %)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
    else:
        
        st.header("Beneficiary Bank statistics")  
        selected_banks = st.multiselect("Select Bank", all_benefit_banks, default = all_benefit_banks[:3])
        
        fig = plt.figure()
        for bank in selected_banks:
            plt.plot(benefit_months, benefit_bank_monthly_volume[bank], label = bank)
        plt.title("Beneficiary volumes", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("Volume (in Mn)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
        fig = plt.figure()
        for bank in selected_banks:
            plt.plot(benefit_months, benefit_bank_monthly_failure[bank], label = bank)
        plt.title("Beneficiary failures", fontsize = 20)
        plt.xlabel("year",fontsize =16)
        plt.ylabel("failure (in %)",fontsize =16)
        plt.legend()
        st.pyplot(fig)
        
               
     
    
    
