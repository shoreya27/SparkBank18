import json
from .models import Transactions
from datetime import datetime
import pandas as pd
from django.http.response import HttpResponse, JsonResponse
import os
'''
Class TransactionAnalytics
>work in 2 mode
>single customer or multiple customers
>For specific time given
>Need excel sheet in download
'''
mode = ("single","multiple")
class TransactionAnalytics:

    def __init__(self, fromdt, todt, data):
        self.fromdt = datetime.strptime(fromdt,"%Y-%m-%d").date()
        self.todt = datetime.strptime(todt,"%Y-%m-%d").date()
        self.data = data
        self.df = None
    
    def single_customer_specific(self):
        transactions = Transactions.objects.filter(account__customer__phone = self.data,
                                                   created__gte = self.fromdt,
                                                   created__lte = self.todt
                                                    )
        if transactions.count() == 0:
            return
        result = []
        for transaction in transactions:
            temp = []
            name = transaction.account.customer.first_name
            temp.append(transaction.account.customer.phone)
            temp.append(transaction.created)
            temp.append(transaction.action)
            temp.append(transaction.transactionamount)
            temp.append(transaction.currbalance)
            result.append(temp)
        col = ["phone","TransactionDt","Mode", "TransactionAmt", "UpdatedBal"]
        self.df = pd.DataFrame(result, columns = col)        
        print(self.df)
        self.df.to_excel('./transaction.xlsx', sheet_name=name, index=False)    



    def multiple_customer_specific(self):
        #for each customer create a dataframe
        collectn = {}
        for customer in self.data:
            #Get all Transactions from this customer
            transactions = Transactions.objects.filter(account__customer__phone = customer,
                                                    created__gte = self.fromdt,
                                                    created__lte = self.todt
                                                        )
            if transactions.count() == 0:
                continue
            result = []
            name = transactions[0].account.customer.first_name
            for transaction in transactions:
                temp = []
                temp.append(transaction.account.customer.phone)
                temp.append(transaction.created)
                temp.append(transaction.action)
                temp.append(transaction.transactionamount)
                temp.append(transaction.currbalance)
                result.append(temp)
            collectn[name] = None
            col = ["phone","TransactionDt","Mode", "TransactionAmt", "UpdatedBal"]            
            collectn[name] = pd.DataFrame(result, columns = col)

        writer = pd.ExcelWriter('./transaction.xlsx', engine='xlsxwriter')

        for sheet_name in collectn.keys():
            collectn[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()



            
def generate_report(request):
    '''
    GET API FOR TRANSACTION HISTORY
    >FROMDT
    >TODT
    >TYPE ---- SINGLE OR MULTIPLE CUSTOMERS
    >CUSTOMER --- LIST OF CUSTOMER OR CUSTOMERS
    '''
    result = {}
    try:
        data = json.loads(request.body)
        #customers specific or multiple customers
        type = data["type"]
        if type not in mode:
            raise Exception("Invalid Type input:provide single/multiple")
        fromdt = data["fromdt"]
        todt = data["todt"]
        
        #for single customer
        if type == mode[0]:
            customer = data["customers"][0]
            report = TransactionAnalytics(fromdt, todt, customer)
            report.single_customer_specific()
        
        #For multiple customers of bank
        elif type == mode[1]:

            report = TransactionAnalytics(fromdt, todt, data["customers"])
            report.multiple_customer_specific()


        return download_excel()
    except Exception as e:
        result["error_message"] = str(e)
        result["status"] = 500
        result["result"] = "failure "
        return JsonResponse(result, status=result["status"]) 


def download_excel():
        with open("./transaction.xlsx", "rb") as excel:
            data = excel.read()
        response = HttpResponse(data, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="transaction.xlsx"'
        os.remove("./transaction.xlsx")
        return response