from django.shortcuts import render
from django.http.response import JsonResponse
from .models import CustomerAccount, Transactions
import json
from .sendmail import SendMailInterface
# Create your views here.
def enquiry(request, phone):
    '''
    GET API: User Phone is given 
    return User Account Balance
    '''
    result = {}
    try:
        obj = CustomerAccount.objects.get(customer__phone = phone)
        balance = obj.balance
        result["AccountBalance"] = balance
        result["AccountNumber"] = obj.pk
        result["AccountHolderName"] = obj.customer.first_name
        result["result"] = "success"
        result["status"] = 200
    except Exception as e:
        result["error_reason"] = str(e)
        result["result"] = "failure"
        result["status"] = 500
    
    return JsonResponse(result, status =result["status"])


def deposit(request):
    '''
    Find Given user account ,
    Add the given amount to his account---->Increase the balance
    Send the mail
    Return
    '''
    if request.method == "POST":
        result = {}
        try:
            data =json.loads(request.body)
            phone = data["phone"]
            amount = data["deposit_amount"]
            #Fetch User Account
            if int(amount) <= 0:
                raise Exception("Amount should be greated than 0")
            user_wallet = CustomerAccount.objects.get(customer__phone = phone)
            #Increment the balance
            user_wallet.balance += int(amount)
            user_wallet.save()
            #Create Transaction object
            transaction = Transactions(account = user_wallet,action = "credit", 
                                      transactionamount = int(amount),
                                      currbalance = user_wallet.balance 
                                      )
            transaction.save()
            #send mail
            receiver = user_wallet.customer.email
            mail_obj = SendMailInterface(amount,user_wallet.balance,receiver,True)
            mail_obj.sendmail()

            result["result"] = "success"
            result["status"] = 200
        except Exception as e:
            result["error_reason"] = str(e)
            result["result"] = "failure"
            result["status"] = 500
    
        return JsonResponse(result, status =result["status"])


def withdraw(request):
    '''
    Find Given user account ,
    withdraw the given amount to his account
    Only when there is sufficient amount available
    Send the mail
    Return
    '''
    if request.method == "POST":
        result = {}
        try:
            data =json.loads(request.body)
            phone = data["phone"]
            amount = int(data["withdraw_amount"])
            #Fetch User Account
            user_wallet = CustomerAccount.objects.get(customer__phone = phone)

            #check whether this account has sufficient funds
            if user_wallet.balance < amount:
                raise Exception("Sorry!! Insufficent Funds")
            #Increment the balance
            user_wallet.balance -= amount
            user_wallet.save()
            #Create Transaction object
            transaction = Transactions(account = user_wallet,action = "debit", 
                                      transactionamount = amount,
                                      currbalance = user_wallet.balance 
                                      )
            transaction.save()
            #send mail
            receiver = user_wallet.customer.email
            mail_obj = SendMailInterface(amount,user_wallet.balance,receiver,False,True)
            mail_obj.sendmail()

            result["result"] = "success"
            result["status"] = 200
        except Exception as e:
            result["error_reason"] = str(e)
            result["result"] = "failure"
            result["status"] = 500
    
        return JsonResponse(result, status =result["status"])