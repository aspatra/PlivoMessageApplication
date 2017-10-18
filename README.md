# PlivoMessageApplication
Respository is for Plivo message application


This is sample module to to send message from mobile number to another mobile number using Plivo RestApi
and it's web services.

There are some functionality added such as:
1. Once the numbers are bought use message api to send an sms from a number to
another number.One can use both number bought as above to do this.
2. Once message api is successful, response give message uuid.Using this message uuid
get the details of the message using details api.
3. Use pricing api to determine the rate of the message which is outbound rate under
message object in this case.
4. Verify the rate and the price deducted for the sending message, should be same.
5. And finally after sending message, using account details api, account cash credit
should be less than by the deducted amount.
