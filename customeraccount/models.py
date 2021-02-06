from django.db import models

# Create your models here.
'''
customer model should have
>Name
>Phone
>Age
>gender
>email
>city
>pincode
>creationdt
'''

class Customer(models.Model):
    gender = [
        ("male", "male"),
        ("female", "female"),
        ("others", "others")
    ]
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    age = models.IntegerField()
    gender = models.CharField(max_length = 10,choices= gender)
    phone = models.CharField(max_length = 15 )
    email = models.CharField(max_length = 30)
    city = models.CharField(max_length = 20,help_text = "location")
    pincode = models.CharField(max_length = 20,help_text = "pincode")
    # image = models.ImageField(upload_to='customerpic/')
    joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.first_name,self.last_name)

    def get_model_as_json(self):
        d = {}
        d["uniquecustomerid"] = self.pk
        d["firstname"] = self.first_name
        d["lastname"] = self.last_name
        d["age"] = self.age
        d["gender"] = self.gender
        d["phone"] = self.phone
        d["email"] = self.email
        d["city"] = self.city
        d["pincode"] = self.pincode
        d["joining"] = self.joining
        return d

'''
CustomerAccount ---- Wallet of customer
>Linked to a customer FK
>balance
>
'''


class CustomerAccount(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    balance = models.IntegerField(help_text="account balance")
    createdon = models.DateTimeField(auto_now_add=True)     
    lastmodified = models.DateTimeField(auto_now=True)

    def get_model_as_json(self):
        d = {}
        d["accountno"] = self.pk
        d["customer"] = self.customer.get_model_as_json()
        d["balance"] = self.balance
        d["createdon"] = self.createdon
        d["lastmodified"] = self.lastmodified
        return d
    
    def __str__(self):
        return self.customer.phone

'''
Each Transaction Happening will be recorded in Transaction Model
>FK to Customer Account
>action : debit/credit
>transactionamount
>created on : Date
'''
class Transactions(models.Model):
    actions = [
        ("debit","debit"),
        ("credit","credit")
    ]
    account = models.ForeignKey(CustomerAccount,on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=actions)
    transactionamount = models.IntegerField()
    currbalance = models.IntegerField(default=0,help_text="balance currently")
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)