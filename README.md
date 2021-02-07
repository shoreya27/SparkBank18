_**BANKING SOFTWARE ASSIGNMENT**_

# Features
* Customer Registration
* Customer Transactions
  * Money Deposit
  * Money Withdraw
* Email Sent on each transaction to user
* Analytics Report can be downloaded as an Excel
* Enquiry By User

# LETS EXPLORE EACH FEATURE IN DETAIL
# **CUSTOMER REGISTRATION**

_FilePath:customeraccount/CustomerRegistrationInterface_

### POST API
**customer registration** 

``curl --location --request POST 'http://127.0.0.1:8020/customer/register/' \`
`--header 'Content-Type: application/json' \`
`--data-raw '{`
    `"firstname": "shoreya",`
    `"lastname": "gupta",`
    `"age" : "24",`
    `"gender" : "male",`
    `"phone": "9716723882",`
    `"email":"gupta.shoreya2707@gmail.com",`
    `"city":"Delhi",`
    `"pincode":"201011"`

`}'``
**RESPONSE:**

`{`
    `"account_details": {`
        `"accountno": 4,`
        `"customer": {`
            `"uniquecustomerid": 4,`
            `"firstname": "shoreya",`
            `"lastname": "gupta",`
            `"age": "24",`
            `"gender": "male",`
            `"phone": "9716723882",`
            `"email": "gupta.shoreya2707@gmail.com",`
            `"city": "Delhi",`
            `"pincode": "201011",`
            `"joining": "2021-02-06T18:09:08.039Z"`
        `},`
        `"balance": 0,`
        `"createdon": "2021-02-06T18:09:08.048Z",`
        `"lastmodified": "2021-02-06T18:09:08.048Z"`
    `},`
    `"result": "success",`
    `"status": 200`
`}`


# GET API

`curl --location --request GET 'http://127.0.0.1:8020/customer/register/?phone=9716723882'`

### RESPONSE
`{`
    `"data": {`
        `"uniquecustomerid": 4,`
        `"firstname": "shoreya",`
        `"lastname": "gupta",`
        `"age": 24,`
        `"gender": "male",`
        `"phone": "9716723882",`
        `"email": "gupta.shoreya2707@gmail.com",`
        `"city": "Delhi",`
        `"pincode": "201011",`
        `"joining": "2021-02-06T18:09:08.039Z"`
    `},`
    `"result": "success",`
    `"status": 200`
`}`


# TRANSACTION APIS

**POST DEPOSIT API**
* FilePath :customeraccount/views.py
* Increment Balance in user account
* Notify User using Email

`curl --location --request POST 'http://127.0.0.1:8020/customer/deposit/' \`
`--header 'Content-Type: application/json' \`
`--data-raw '{`
    `"phone": "9716723882",`
    `"deposit_amount": 400`
`}'`

## RESPONSE
`{`
    `"result": "success",`
    `"status": 200`
`}`

**POST WITHDRAW API**
* FilePath :customeraccount/views.py
* Decrement Balance in user account only if there is sufficient fund available
* Notify User using Email

`curl --location --request POST 'http://127.0.0.1:8020/customer/withdraw/' \`
`--header 'Content-Type: application/json' \`
`--data-raw '{`
    `"phone": "9716723882",`
    `"withdraw_amount": 330`
`}'`

## RESPONSE
`{`
    `"result": "success",`
    `"status": 200`
`}`

# ENQUIRY BY USER ABOUT ACCOUNT BALANCE

**GET ENQUIRY API**
* FilePath : customeraccount/views.py
* View Name: enquiry()
* Returns user account banlance and information

**CURL**
`curl --location --request GET 'http://127.0.0.1:8020/customer/enquiry/9716723882'`

**RESPONSE**
`{`
    `"AccountBalance": 64820,`
    `"AccountNumber": 4,`
    `"AccountHolderName": "shoreya",`
    `"result": "success",`
    `"status": 200`
`}`


# REPORT API

**DOWNLOAD EXCEL REPORT API**
* FilePath : customeraccount/analytics.py
* View Name : generate_report
* Manager can download excel for specific time period
* Report can be created for Single User or Multiple Users

**CURL**
# SPECIFIC USER IN TIMEFRAME
`curl --location --request GET 'http://127.0.0.1:8020/customer/report/' \`
`--header 'Content-Type: application/json' \`
`--data-raw '{`
    `"type":"single",`
    `"fromdt": "2021-02-06",`
    `"todt": "2021-02-06",`
    `"customers": [ "9716723882"]`
`}'`


# MULTIPLE USER IN TIMEFRAME
`curl --location --request GET 'http://127.0.0.1:8020/customer/report/' \`
`--header 'Content-Type: application/json' \`
`--data-raw '{`
    `"type":"multiple",`
    `"fromdt": "2021-02-06",`
    `"todt": "2021-02-06",`
    `"customers": [ "9716723882", "7000020000"]`
`}'`


