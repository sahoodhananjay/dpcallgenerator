import pandas as pd
import numpy as np
#from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import time
from numpy.random import randint
import multiprocessing
import concurrent.futures

import warnings
warnings.filterwarnings("ignore")

## Define all input parameters for the test

## Test user1 launched on Browser: On Chrome Canary
first_authorization = 'Bearer 3jzesv2sZKfNtTTsNCKhEsQNAJ8dXwN86E6tfNbkb35z8ttwRRGVnuWtUbHjDtEMDqJXLGP73S77JnCk6BujMgsxHhY2Pa6nTxeJ'
first_calling_party = '6239542718496768'   #testdialpad_ms
first_called_party = "+14242508641"  #"+14062953682"        #Auto_Perf_3
first_contact_key = "aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgIDInJWHtgoM" #"aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgICwjZriuQsM"   #Auto_Perf_3
first_target_key = "aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICAsPrL2ooLDA"    #testdialpad_ms

## Test user2 launched onBrowser: On Chrome Beta
second_authorization = 'Bearer wpfhUUc42sV9JQ2ksHaSVnVS6YwxxU4E3tQGDbG2XnpdXHE5hC96C7cDev5QBYUsnPzN4abDNNf5BwNx7mwY6gbEWRAKzQKYmuxH'
second_calling_party = '5955753775202304'   #PD Test
second_called_party = "+14242466983"        #Auto_Perf_1
second_contact_key = "aglzfnV2LWJldGFyZAsSB0NvbnRhY3QiV2h0dHA6Ly93d3cuZ29vZ2xlLmNvbS9tOC9mZWVkcy9jb250YWN0cy9wb3dlcmRpYWxlcnRlc3RAZ21haWwuY29tL2Jhc2UvNWYzYTZjMmQ4YmYwNTZjMQw"  #Auto_Perf_1
second_target_key = "aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICAkOGfl8oKDA"    #PD Test

## Test user3 launched on Browser: On MS Edge
third_authorization = 'Bearer a3WyhL9rNc7c3duJMBWm2cLkuGeXcqmMAZm3XWCHtAfXGmDfyXQ5vMnycsCtAFM9jnnyaRcq47kX7V3EUXnbvDnS3XdVk2ScmWxp'
third_calling_party = '4522934864969728'   #Testdialpad1
third_called_party = "+14242506968"        #Auto_Perf_2
third_contact_key = "aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgICwk7ydvwgM"   #Auto_Perf_2
third_target_key = "aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICA4K_dsoQIDA"    #Testdialpad1

## Test user4 launched on Browser: On Ingonito
fourth_authorization = 'Bearer L8cS8N26Nvwxf3ybMuCMpYceS7LjxYrPqXMKSMZBycPYbFEjghwjUZQUeF3Kv49KRQh3s9gqV5V8uZvNkmmVjXC3D2xJafBRUCRK'
fourth_calling_party = '5006542366310400'   #Testdialpad11
fourth_called_party = "+14244378677"        #Auto_Perf_4
fourth_contact_key = "aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgIDI_IDt_QkM"   #Auto_Perf_4
fourth_target_key = "aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICAsNrHrfIIDA"    #Testdialpad11

#Browser: On Ingonito
#fifth_authorization = 'Bearer MYNGV9HWtXM2cCCePjgQARxvrfKt6BCr4wGfWYrxqKYBdk5ALQSbU9FZVr3QZswWTwDZjLr8PeRtMPdbdU7XEjvWvKQ2YPZ92SRH'
#fifth_calling_party = '4793537943306240'   #Testdialpad
#fifth_called_party = "+12242449974"        #Auto_Perf_5
#fifth_contact_key = "aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgICwk7ydvwgM"   #Auto_Perf_4
#fifth_target_key = "aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICA4K_dsoQIDA"    #Testdialpad11



main_apikey = "ULLc7YuA4S47aCKzKufM5NbBZr8jgqgvjJLDrwHfZjSQYwBJ2DGxsexzEVNVevsMvxTZwLn5cLA7mTT95HZhS7HhQq4M2H4yUhg9"
note = "Call logging"
subject = "Performance Test"
iteration = 6
calling_url = "https://dialpadbeta.com/api/v2/users/"

## This function use Dialpad public API to make outbound call. The function uses real Dialpad webclient as the test user.

def make_call(apikey,authorization,called_party,calling_party):
    
    startcall_url = calling_url+calling_party+"/initiate_call?apikey=" + apikey   

    print("Make Call API:", startcall_url)
    header = {
        'authority': 'dialpadbeta.com',
        'User-Agent': 'PostmanRuntime/7.26.8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'authorization': authorization,
        'referer': 'https://dialpadbeta.com/'
    }
    body = {
        "phone_number": called_party,
    }

    try:
        startcall_r = requests.post(startcall_url, data=json.dumps(body), headers=header)
        startcall_soup = BeautifulSoup(startcall_r.content, 'html5lib')
        startcall_content = startcall_soup.get_text()
        startcall_json_content = json.loads(startcall_soup.text)
        print("Calling Response Code From Server:",startcall_r.status_code)
        
        if startcall_r.status_code == 200:
            time.sleep(3)

            callstatus_url = calling_url+calling_party+"/togglevi?apikey=" + apikey            
            print("Call Status API:", callstatus_url)
            header = {
                'authority': 'dialpadbeta.com',
                'User-Agent': 'PostmanRuntime/7.26.8',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'content-type': 'application/json',
                'authorization': authorization,
                'referer': 'https://dialpadbeta.com/'
            }

            try:
                callstatus = ''
                ringingState = 0
                while callstatus != 'connected':
                    ringingState += 1
                    callstatus_r = requests.patch(callstatus_url, headers=header)
                    if callstatus_r.status_code != 200:
                        callstatus_soup = BeautifulSoup(callstatus_r.content, 'html5lib')
                        callstatus_content = callstatus_soup.get_text()
                        callstatus_json_content = json.loads(callstatus_soup.text)
                        print("Status Failed:",callstatus_json_content)
                        error_msg = callstatus_json_content['error']['errors'][0]['message']

                        file_name = "performance_calllogging_" + calling_party + ".csv"
                        
                        time.sleep(3)
                        if ringingState == 3:
                            with open(file_name, 'a', encoding="utf-8", newline='') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(error_msg)
                                csvFile.close()
                            return 3

                    else:
                        callstatus_soup = BeautifulSoup(callstatus_r.content, 'html5lib')
                        callstatus_content = callstatus_soup.get_text()
                        callstatus_json_content = json.loads(callstatus_soup.text)
                        callstatus = callstatus_json_content["call_state"]
                        #print("Calling Status: {}".format(callstatus))
                        if callstatus == 'connected':
                            call_id = callstatus_json_content["id"]
                            print("Calling Status: {} and call-id: {}".format(callstatus,call_id))

                    time.sleep(1)

            except Exception as e:
                print("Status Oops!", e.__class__, "occurred.")

            time.sleep(45)
            return 0

        else:
            startcall_soup = BeautifulSoup(startcall_r.content, 'html5lib')
            startcall_content = startcall_soup.get_text()
            startcall_json_content = json.loads(startcall_soup.text)
            print("Call Failed:", startcall_json_content)
            error_msg = startcall_json_content['error']['errors'][0]['message']

            file_name = "performance_calllogging_" + calling_party + ".csv"
            with open(file_name, 'a', encoding="utf-8", newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(error_msg)
                csvFile.close()
            time.sleep(45)
            return 1

    except Exception as error:
        print("Calling Error!", error.__class__, "occurred.")


## This function use Dialpad private API to log call activity to Salesforce.

def log_call_activity(count,call_id,authorization,contact_key,target_key,note,subject,calling_party):
    
    calllog_url = 'https://dialpadbeta.com/api/salesforcenote/'
    print("Call Activity Logging API:", calllog_url)
    header = {
        'authority': 'dialpadbeta.com',
        'User-Agent': 'PostmanRuntime/7.26.8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': authorization,
        'referer': 'https://dialpadbeta.com/',
        'content-type': 'application/json'
    }
    body = {
        "call_id": call_id,
        "contact_key": contact_key,
        "note": note + "_" + str(count) + ", Calling Party ID: " + calling_party,
        "subject": subject + "_" + str(count),
        "target_key": target_key
    }
    try:
        r = requests.post(calllog_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        json_content = json.loads(soup.text)
        print(r.status_code)
        print(json_content)
        # response_data = json_content["phone_numbers"]
        return r.status_code, json_content

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return 0, 0

## This function use Dialpad private API to retrieve call activity from Salesforce.

def retrieve_call_activity(count,authorization,contact_key,target_key,calling_party):

    retrieve_url = "https://dialpadbeta.com/api/integrations/salesforce?contact_key=" + contact_key + "&service=salesforce&target_key=" + target_key
    print("Retrieve Call Activity API:", retrieve_url)
    header = {
        'authority': 'dialpadbeta.com',
        'User-Agent': 'PostmanRuntime/7.26.8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': authorization,
        'referer': 'https://dialpadbeta.com/'
    }

    try:
        r = requests.get(retrieve_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        json_content = json.loads(soup.text)
        print(r.status_code)
        #print(json_content)

        if (r.status_code == 200):
            activity_subject = json_content["data"]["activity_history"][0]["Subject"]
            activity_description = json_content["data"]["activity_history"][0]["Description"]
            #print(activity_subject, activity_description)

            if ((activity_subject == "Performance Test_" + str(count)) and (
                    activity_description == "Call logging_" + str(count) + ", Calling Party ID: " + calling_party)):
                return r.status_code, True
            else:
                return r.status_code, False

        else:
            return r.status_code, False

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        return 0, False


## Function that starts the load test.

def start_test(iteration,apikey,authorization,called_party,calling_party,note,subject,contact_key,target_key):
    failurecall = 0
    successfullcall = 0
    exceptioncall = 0
    count = 1
    while count < iteration:
        makecall = make_call(apikey, authorization, called_party, calling_party)
        if makecall == 1:
            failurecall += 1
            print("For user: {} - Total Fail Calls: {}".format(calling_party,failurecall))

        if makecall == 0:
            successfullcall += 1
            print("For user: {} - Total Successful Calls: {}".format(calling_party,successfullcall))

        if makecall == 3:
            exceptioncall += 1
            print("For user: {} - Total Status Failure: {}".format(calling_party,exceptioncall))


        print("Completed Call for user {}: count - {}.".format(calling_party,count))
        count += 1

    return successfullcall,failurecall,exceptioncall


## Main function to initiate 4 Dialpad outbound calls in parallel 
if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        p1 = executor.submit(start_test, iteration, main_apikey, first_authorization, first_called_party,
                            first_calling_party, note, subject, first_contact_key, first_target_key)
        p2 = executor.submit(start_test, iteration, main_apikey, second_authorization, second_called_party,
                             second_calling_party, note, subject, second_contact_key, second_target_key)
        p3 = executor.submit(start_test, iteration, main_apikey, third_authorization, third_called_party,
                             third_calling_party, note, subject, third_contact_key, third_target_key)
        p4 = executor.submit(start_test, iteration, main_apikey, fourth_authorization, fourth_called_party,
                             fourth_calling_party, note, subject, fourth_contact_key, fourth_target_key)
        #p5 = executor.submit(start_test, iteration, main_apikey, fifth_authorization, fifth_called_party,
        #                     fifth_calling_party, note, subject, fifth_contact_key, fifth_target_key)


    print('\n*********** Load Test Summary ***********')
    print("Result For testdialpad_ms (Success, Fail, Status): ", p1.result())
    print("Result For PD Test (Success, Fail, NoAnswer): ", p2.result())
    print("Result For testdialpad1 (Success, Fail, Status): ", p3.result())
    print("Result For testdialpad11 (Success, Fail, Status): ", p4.result())
    



