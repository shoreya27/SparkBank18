from django.views import View
import json
from django.http.response import JsonResponse
import re
from .models import CustomerAccount, Customer


'''
Class Based View for customer account opening in Spark18 bank
This will handle post/get request .
REST API
'''

class CustomerRegisteration(View):

    def get(self, request):
        result = dict()
        try:
            customer_id = request.GET["phone"]
            obj = Customer.objects.filter(phone=customer_id)
            if obj:
                result["data"] = obj[0].get_model_as_json()
            else:
                raise Exception("No such entry found")
            result["result"] = "success"
            result["status"] = 200
        except Exception as e:
            result["error_reason"] = str(e)
            result["result"] = "failure"
            result["status"] = 500
        return JsonResponse(result, status = result["status"])

    def post(self, request):
        result = dict()
        try:
            data = json.loads(request.body)
            first_name = data["firstname"]
            last_name = data["lastname"]
            if not data["age"].isnumeric():
                raise Exception("Inappropriate Age")
            age = data["age"]
            gender = data["gender"].lower() #male , female , other
            if not self.isvalid(data["phone"]):
                raise Exception("Inappropriate phone")
            #check whether this user is already registered
            #if yes , dont allow for other registration
            if  self.check_user_existence(data["phone"]):
                raise Exception("This phone is already registered.")
            phone = data["phone"]
            email = data["email"]
            city = data["city"]
            pincode = data["pincode"]
            #Account Registeratin in Our Bank
            customer_obj = Customer(
                                            first_name = first_name,
                                            last_name = last_name,
                                            age = age,
                                            gender = gender,
                                            phone = phone,
                                            email = email,
                                            city = city,
                                            pincode = pincode
                                            )
            customer_obj.save()

            #Account is registered successfully
            #Lets open Bank Wallet Account

            customer_wallet_obj = CustomerAccount(
                                                customer = customer_obj,
                                                balance = 0
                                        )
            customer_wallet_obj.save()

            balance = customer_wallet_obj.get_model_as_json()


            result["account_details"] = balance
            result["result"] = "success"
            result["status"] = 200
        except Exception as e:

            result["account_details"] = {}
            result["error_reason"] = str(e)
            result["result"] = "failure"
            result["status"] = 500
        return JsonResponse(result, status = result["status"])
    
    def isvalid(self,phone):
        Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
        return Pattern.match(phone) 

    def check_user_existence(self,phone):
        user = Customer.objects.filter(phone = phone)
        if user:
            return True
        return False