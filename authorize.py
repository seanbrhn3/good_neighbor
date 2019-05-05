from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*
import pymongo
client = pymongo.MongoClient("mongodb+srv://seanbrhn3:45305006@goodneighbordb-1pr3o.mongodb.net/test?retryWrites=true")
db = client.test
class Auth():
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name ='29mBg5SW'
    merchantAuth.transactionKey ='3F6xd6DY7E8gP44E'

    def creds(self, cardNumber,exp_date,amount_to_take):
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber =cardNumber
        creditCard.expirationDate =exp_date

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType ="authCaptureTransaction"
        transactionrequest.amount = Decimal (amount_to_take)
        transactionrequest.payment = payment


        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = self.merchantAuth
        createtransactionrequest.refId ="MerchantID-0001"

        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if (response.messages.resultCode=="Ok"):
               print("Transaction ID : %s"% response.transactionResponse.transId)
        else:
               print("response code: %s"% response.messages.resultCode)
    def deleteAll(self):
        return db.userInfo.remove()
    def deletePool(self):
        return db.pool.remove()
    def pool(self):
        return db.pool.find()
    def deleteVotes(self):
        return db.vote.remove()
