import json
import requests
from urllib.request import Request,urlopen
from requests.auth import HTTPDigestAuth
from base64 import b64encode
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth


class PlivoMsgApplication(object):



    def __init__(self, auth_id, auth_token,api_id):
        self.has_authed = False
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.api_id = api_id
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0'

    def auth(self):

        if self.has_authed == False:
            self.auth()

        url = 'https://api.plivo.com/v1'

        response = requests.get(url,auth=HTTPDigestAuth(self.auth_id,self.auth_token), verify=True)
        if (response.ok):
            jData = json.loads(response.content)

            print("The response contains {0} properties".format(len(jData)))
            print("\n")
            for key in jData:
                print(key + " : " + jData[key])
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()




    #send message method takes
    #source, destination, text data as mandatory parameter
    def send_message(self,src,dst,text):
        url = 'https://api.plivo.com/v1/Account/{0}/Message/'.format(self.auth_id)

        params = {
            'src':src,
            'dst':dst,
            'text':text,
            'method':'POST'
        }

        #cash_credit is needed to verify the amount present in account
        url_account = 'https://api.plivo.com/v1/Account/{}/'.format(self.auth_id)
        response_account = requests.get(url_account, auth = (self.auth_id,self.auth_token))
        jData = json.loads(response_account.text)
        cash_credit = jData['cash_credits']

        response =requests.post(url, json=params, auth=(self.auth_id, self.auth_token))

        if (response.ok):
            jData = json.loads(response.content)
            self.verify_transaction_account(cash_credit,jData['message_uuid'])
            print("The response contains {0} properties".format(len(jData)))
            print("\n")
            print(jData)

        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    #This method gives the message the user is enquiring for.
    #mandatory parameter message_uid
    def get_message(self,message_uid):
        url = 'https://api.plivo.com/v1/Account/{0}/Message/{1}/'.format(self.auth_id,message_uid)

        param = {'method':'GET'}
        response = requests.get(url, json =param, auth=(self.auth_id,self.auth_token) )

        if (response.ok):
            jData = json.loads(response.text)
            print(jData)
            return jData

        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()



    #this function gives the charges deducted for sending the message
    def get_price(self,country_iso):
        url = 'https://api.plivo.com/v1/Account/{}/Pricing/'.format(self.auth_id)
        param ={
            'country_iso': country_iso,
            'method' : 'GET'
        }

        response = requests.get(url, params=param, auth=(self.auth_id,self.auth_token))
        #print(response.content)

        if (response.ok):
            jData = json.loads(response.text)


            print("The response contains {0} properties".format(len(jData)))
            print("\n")
            for key,value in jData.items():
                if key == "message":
                    rate = jData[key]['outbound']
                    return (rate)

        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    #This method verify the transaction for a given message_uid
    def verify_rate(self,country_iso,message_uid):
        message_data = self.get_message(message_uid)
        charges = self.get_price(country_iso)
        if message_data['total_amount'] == charges['rate']:
            print('You are charged correctly')
        else:
            print('Charges differed,contact customer care for more information!')




    #This method verify account deduction charges for a message
    def verify_transaction_account(self, cash_credit,message_uuid):

        message_uuid = ''.join(message_uuid)
        jData_amount = self.get_message(message_uuid)
        amount_deducted = jData_amount['total_amount']

        url_account = 'https://api.plivo.com/v1/Account/{}/'.format(self.auth_id)
        response_account = requests.get(url_account, auth = (self.auth_id,self.auth_token))
        jData = json.loads(response_account.text)
        cash_credit_new = jData['cash_credits']

        if float(cash_credit_new) == (float(cash_credit)-float(amount_deducted)):
            print('New account cash credit is less than by the deducted amount.')










if __name__ == '__main__':
    obj = PlivoMsgApplication('MANGUYY**********','ODAxYjViNTZiMG***********************','6fa7a7be-b331-11e7-8edf-02ed609bd62b')
    #obj.auth()
    obj.send_message('+1 540-253-1898','+1 213-431-0959','Testing Api')
    #obj.get_message('46f2c0d6-b365-11e7-b886-067c5485c240')
    #obj.get_price('US')
    #obj.verify_rate('US', '46f2c0d6-b365-11e7-b886-067c5485c240')


