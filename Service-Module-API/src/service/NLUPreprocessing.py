# import urllib.request
# import json
# import os
# import ssl
# from model.response.GeneralResponse import generalResponse

# class nluPreprocessing:        
#     def intentClassificationModel(self,  message : str):
#         # TODO : logic for call service class
#         print("IC lanjut")
#         return message
        
#     def NamedEntityRecognitionModel(self,  message : str):
#         print("NER lanjut")
#         return message

#     def LLM(self,  message : str):
#         # TODO : LLM 2nd Service bakal dibikinin endpoint
#         def allowSelfSignedHttps(allowed):
#             if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
#                 ssl._create_default_https_context = ssl._create_unverified_context

#         allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
#         data = {
#             "input_data": {
#                 "input_string": [
#                     {
#                         "role": "user",
#                         "content": "Hello there!"
#                     },
#                     {
#                         "role": "assistant",
#                         "content": "Hell there!, welcome to digital bank customer service, how i can assist you today?."
#                     },
#                     {
#                         "role": "user",
#                         "content": f"{message}"
#                     }
#                 ],
#                 "parameters": {
#                     "temperature": 0.6,
#                     "top_p": 0.9,
#                     "do_sample": True,
#                     "max_new_tokens": 200,
#                     "return_full_text": False
#                 }
#             }
#         }

#         body = str.encode(json.dumps(data))

#         url = 'https://calvink-bqppl.eastus2.inference.ml.azure.com/score'
#         # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
#         api_key = 'hUZqXNKwsZXFF0tzLab56HV7wssdmaRa'
#         if not api_key:
#             raise Exception("A key should be provided to invoke the endpoint")

#         # The azureml-model-deployment header will force the request to go to a specific deployment.
#         # Remove this header to have the request observe the endpoint traffic rules
#         headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'mistralai-mistral-7b-instruct-9' }

#         req = urllib.request.Request(url, body, headers)

#         try:
#             response = urllib.request.urlopen(req)
#             result = response.read()
#             decoded_output = result.decode('utf-8')
#             parsed_output = json.loads(decoded_output)
#             output_value = parsed_output["output"]
#             return output_value
#         except urllib.error.HTTPError as error:
#             print("The request failed with status code: " + str(error.code))
#             print(error.info())
#             print(error.read().decode("utf8", 'ignore'))