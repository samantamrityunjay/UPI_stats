
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import calendar
from datetime import datetime

from upi_product import upi_product
from upi_ecosystem import upi_ecosystem

url_product = "https://www.npci.org.in/what-we-do/upi/product-statistics"
url_ecosystem = "https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics"


st.title("UPI statistics")

@st.cache
def get_data(url_product,url_ecosystem):
    data_upi_product = upi_product(url_product).data()
    
    monthly_ecosystem_stat = upi_ecosystem(url_ecosystem).months_data()
    
    return data_upi_product, monthly_ecosystem_stat

data_upi_product, monthly_ecosystem_stat = get_data(url_product, url_ecosystem)



@st.cache
def get_upi_app_data(monthly_ecosystem_stat):
    months = [datetime.strptime(x, '%b %Y') for x in monthly_ecosystem_stat.keys() if "upi_app_stat" in monthly_ecosystem_stat[x].keys()]
    
    all_upi_apps = list(set([app for x in monthly_ecosystem_stat.keys() if "upi_app_stat" in monthly_ecosystem_stat[x].keys() for app in monthly_ecosystem_stat[x]["upi_app_stat"]["AppName"]]))
    
    upi_app_monthly_value = {}
    upi_app_monthly_volume = {}
    for app in all_upi_apps:
        upi_app_monthly_value[app] = [monthly_ecosystem_stat[key]["upi_app_stat"]["TotalValue"][monthly_ecosystem_stat[key]["upi_app_stat"]["AppName"].index(app)] if app in monthly_ecosystem_stat[key]["upi_app_stat"]["AppName"] else 0 for key in monthly_ecosystem_stat.keys() if "upi_app_stat" in monthly_ecosystem_stat[key].keys()]
        
        upi_app_monthly_volume[app] = [monthly_ecosystem_stat[key]["upi_app_stat"]["TotalVolume"][monthly_ecosystem_stat[key]["upi_app_stat"]["AppName"].index(app)] if app in monthly_ecosystem_stat[key]["upi_app_stat"]["AppName"] else 0 for key in monthly_ecosystem_stat.keys() if "upi_app_stat" in monthly_ecosystem_stat[key].keys()]
        
    return months, all_upi_apps, upi_app_monthly_value, upi_app_monthly_volume

upi_months, all_upi_apps, upi_app_monthly_value, upi_app_monthly_volume = get_upi_app_data(monthly_ecosystem_stat)

@st.cache
def get_remit_bank_data(monthly_ecosystem_stat):
    months = [datetime.strptime(x, '%b %Y') for x in monthly_ecosystem_stat.keys()]
    
    all_remit_banks = list(set([bank for month in monthly_ecosystem_stat.keys() for bank in monthly_ecosystem_stat[month]['remitter_bank']["BankName"]]))
    
    remit_bank_monthly_volume = {}
    remit_bank_monthly_failure = {}
    for bank in all_remit_banks:
        remit_bank_monthly_volume[bank] = [monthly_ecosystem_stat[key]["remitter_bank"]["TotalVolume"][monthly_ecosystem_stat[key]["remitter_bank"]["BankName"].index(bank)] if bank in monthly_ecosystem_stat[key]["remitter_bank"]["BankName"] else 0 for key in monthly_ecosystem_stat.keys()]
        
        remit_bank_monthly_failure[bank] = [100 - monthly_ecosystem_stat[key]["remitter_bank"]["Approved"][monthly_ecosystem_stat[key]["remitter_bank"]["BankName"].index(bank)] if bank in monthly_ecosystem_stat[key]["remitter_bank"]["BankName"] else 0 for key in monthly_ecosystem_stat.keys()]
        
    return months, all_remit_banks, remit_bank_monthly_volume, remit_bank_monthly_failure

remit_months, all_remit_banks, remit_bank_monthly_volume, remit_bank_monthly_failure = get_remit_bank_data(monthly_ecosystem_stat)


@st.cache
def get_benefit_bank_data(monthly_ecosystem_stat):
    months = [datetime.strptime(x, '%b %Y') for x in monthly_ecosystem_stat.keys()]
    
    all_benefit_banks = list(set([bank for month in monthly_ecosystem_stat.keys() for bank in monthly_ecosystem_stat[month]['beneficiary_bank']["BankName"]]))
    
    benefit_bank_monthly_volume = {}
    benefit_bank_monthly_failure = {}
    for bank in all_benefit_banks:
        benefit_bank_monthly_volume[bank] = [monthly_ecosystem_stat[key]["beneficiary_bank"]["TotalVolume"][monthly_ecosystem_stat[key]["beneficiary_bank"]["BankName"].index(bank)] if bank in monthly_ecosystem_stat[key]["beneficiary_bank"]["BankName"] else 0 for key in monthly_ecosystem_stat.keys()]
        
        benefit_bank_monthly_failure[bank] = [100 - monthly_ecosystem_stat[key]["beneficiary_bank"]["Approved"][monthly_ecosystem_stat[key]["beneficiary_bank"]["BankName"].index(bank)] if bank in monthly_ecosystem_stat[key]["beneficiary_bank"]["BankName"] else 0 for key in monthly_ecosystem_stat.keys()]
        
    return months, all_benefit_banks, benefit_bank_monthly_volume, benefit_bank_monthly_failure

benefit_months, all_benefit_banks, benefit_bank_monthly_volume, benefit_bank_monthly_failure = get_benefit_bank_data(monthly_ecosystem_stat)   
       
    

type_statistic = st.sidebar.selectbox("Type of statistics",("Overall UPI product", "UPI Ecosystem"))

if type_statistic == "Overall UPI product":
    st.header("Overall UPI product statistics")
    
    st.markdown("### Bank statistics")            
    fig,ax = plt.subplots(figsize = (16,9))
    ax.bar(data_upi_product.iloc[:,0], data_upi_product.iloc[:,1], color = 'r')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval= 2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    plt.xticks(rotation = 90)
    plt.title("No. of banks live on UPI", fontsize= 20)
    plt.ylabel("No. of banks", fontsize= 14)
    plt.xlabel("Year", fontsize= 14)   
    st.pyplot(fig)
    
    st.markdown("### Volume and Value of transactions")
    fig,ax = plt.subplots(figsize = (16,9))
    s = [0.5*x for x in data_upi_product.iloc[:,2]]
    ax.scatter(data_upi_product.iloc[:,0], data_upi_product.iloc[:,2], s = s, color = 'r')
    ax.set_xlabel("year",fontsize=16)
    ax.set_ylabel("Volume (in Mn)",color="red",fontsize=16)
    
    ax2=ax.twinx()
    ax2.plot(data_upi_product.iloc[:,0], data_upi_product.iloc[:,3], color = 'b')
    ax2.set_xlabel("year",fontsize=16)
    ax2.set_ylabel("Value (in Cr)",color="blue",fontsize=16)
    
    plt.title("Volume and value of transactions on UPI", fontsize=20)
    
    st.pyplot(fig)
    
    
    st.markdown("### UPI Product data")
    st.write(data_upi_product)
    
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
        
               
     
    
    
