#!/usr/bin/python3
import json
import numpy as np
import re


def getJson(jsonFile):
    ''' Function to return a json object from file. File must contain JSON, returns JSON object 
        getJson(jsonFile)
        jsonFile -> a json file'''
    # Open file
    f = open(jsonFile)
    # Load JSON data from file
    data = json.load(f)

    return data

def writeJson(jsonFile, data):
    ''' Function to format and write JSON to a file
        writeJson(jsonFile, data)
        jsonFile-> file to write json to
        data-> dic that will be formated as json and written to the file'''
    with open(jsonFile, "w") as wf:
        json.dump(data, wf, indent=2)


def writeMailGun(mailFile, data):
    ''' Function that adds correctly formatted entries to the mail.ini file
        writeMailGun(mailFile, data)
        mailFile-> file to update
        data -> array of org ids to add to file
    '''
    with open(mailFile, "a") as wf:
        for id in data:
            wf.write("\n[dd.mail.transport:org_" + str(id) + "]\n" )
            wf.write("method=mailgun\n")



def checkNum(numArray, hipaaArray, file, trace=False):
    ''' Function to check if values in 1st array (numArray) exist in 2nd array (hipaaArray). 
        Returns array with elements from 1st (numArray) array that are not in the 2nd array (hipaaArray) (i.e. values that need to be added to the second array).
        checkNum(numArray, hipaaArray, file, trace=False)
        numArray -> array of values to see if they are in hipaaArray
        hipaaArray -> array of values for numArray to check against
        file -> String to denote the file that is being checked (i.e. what the hipaaArray was generated from)
        returns a new array of only values from numArray that are NOT in hipaa array'''

    newArray=[]
    if trace:
        print("Checking list: " + str(numArray))
        print("Against list: " + str(hipaaArray))
    
    for num in numArray:
        if int(num) not in hipaaArray:
            newArray.append(num)
        else:
            print("Org ID " + str(num) + " is already in " + file)
     
    if trace:
        print("Numbers to be updated: ")
        for id in newArray:
            print(id)
        

    return newArray

def orgIdArray(file, trace=False):
    '''
    '''
    file_array=[]
    sorted_array=[]

    with open(file) as f:
        for line in f:
            file_array.append(int(line.strip('\n')))
        arr = np.array(file_array)
        sorted_array=np.sort(arr)
    
    if trace:
        print(file_array)
        print(sorted_array)

    return sorted_array


def createFileArray(file, trace=False):
    ''' Takes in ** mail.ini ** file and writes each line to an array (for non json files) 
        createFileArray(file, trace=False)
        file -> A txt file that will have each line split into an array
        trace -> default false, when set to true will print debug information '''

    file_array=[]

    with open(file) as f:
        for line in f:
            if (is_string_match(line)):
                file_array.append(line)

    if trace:
        for l in file_array:
            print(l)

    return file_array

def cleanUpMailIniArray(ary, trace=False):
    ''' Takes in mail.ini file as an array, '''
    mail_array=[]

    for i in ary:
        num = re.findall(r'\d+', i)
        if len(num) > 0:
            mail_array.append(int(num[0]))
            if trace:
                print(num[0])

    return mail_array

def is_string_match(string: str) -> bool:
    # Use a regular expression to match the pattern
    pattern = r"\[dd\.mail\.transport:org_"
    return bool(re.match(pattern, string))

def insert_num_in_order(numToBeAdded, hipaaArray, trace=False):
    ''''''
    if trace:
        print("Array to be added: " + str(numToBeAdded))
        print("Hipaa Array: " + str(hipaaArray))

    indOne = 0
    indTwo = 0
    newArray = []
    ntba_length = len(numToBeAdded)
    ha_length = len(hipaaArray)

    while indOne < ntba_length:
        if ha_length <= indTwo:
            if int(numToBeAdded[indOne]) not in newArray:
                newArray.append(int(numToBeAdded[indOne]))
            indOne+=1
        
        elif int(numToBeAdded[indOne]) < int(hipaaArray[indTwo]):
            if int(numToBeAdded[indOne]) not in newArray:
                newArray.append(int(numToBeAdded[indOne]))
            indOne+=1
            
        else:
            if int(hipaaArray[indTwo]) not in newArray:
                newArray.append(int(hipaaArray[indTwo]))
            indTwo+=1

    while indTwo < ha_length:
        newArray.append(int(hipaaArray[indTwo]))
        indTwo+=1




    if trace:
        print("newArray: " + str(newArray))

    return newArray

def dups(array):
    nArray=[]
    for i in array:
        if i not in nArray:
            nArray.append(i)
        else:
            print("Duplicate found: " + str(i))


def main():

    # Get Directory from user and remind them to create a branch before continueing:
    print("Make sure a branch is created before you proceed, do not work out of the master branch")
    print("Enter the full directory path to your datadog")
    repo=input("Example: /Users/username/DDrepos/consul-config/datadog/us1.prode.dog/: ")
    
    '''Remember when creating org file:
        1,100,xxx,xxx is Govcloud
        1,000,000,000 is EU
        1,200,000,000 is US3
        1,300,000,000 is US5
        
        These different id ranges will need to be seperated out and addressed in seperate runs of the script.
        Github is setup so that you can not update more that one env at a time.'''
    
    # Get org ids
    org_dir=input("Enter directory and file of list for org id's: ")

    # Create an org id array
    org_ids=orgIdArray(org_dir, False)
    print(org_ids)
    # Traces are set for debugging
    trace = False
    trace_array_lists = False
    trace_array_lists_two = False

    # Compare all org ids in the hipaa_compliance file and generate array that needs to be added
    # get array from current hipaa_compliance file
    hipaa_compliance_array = getJson(repo+"features/hipaa_compliance")
    # compare current array to new array
    hipaa_compliance = checkNum(org_ids, hipaa_compliance_array['enabled_orgs'], "hipaa_compliance", trace)
    
    # Compare all org ids in the expanded_hipaa_compliance and generate an array that needs to be added
    # get array from current expanded_hipaa_compliance file
    expanded_hipaa_compliance_array = getJson(repo+"features/expanded_hipaa_compliance")
    # compare current array to new array
    expanded_hipaa_compliance = checkNum(org_ids, expanded_hipaa_compliance_array['enabled_orgs'], "expanded_hipaa_compliance", trace)

    # Compare all org ids in mail.ini and generate array that needs to be added
    mail_text_array = createFileArray(repo+"consul_config/mail.ini", trace)
    mail_array = cleanUpMailIniArray(mail_text_array)
    mail = checkNum(org_ids, mail_array, "mail.ini", trace)

    if trace_array_lists:
        print("hipaa_compliance: " + str(hipaa_compliance))
        print("expanded_hipaa_compliance: " + str(expanded_hipaa_compliance))
        print("mail: " + str(mail))

    # Generate updated arrays with all org ids in numerical order (less mail.ini)
    final_hipaa_compliance_array = insert_num_in_order(hipaa_compliance, hipaa_compliance_array['enabled_orgs'], trace)
    final_expanded_hipaa_compliance_array = insert_num_in_order(expanded_hipaa_compliance, expanded_hipaa_compliance_array['enabled_orgs'], trace)
    #final_mail = insert_num_in_order(mail, mail_array, trace)

    dups(final_hipaa_compliance_array)
    dups(final_expanded_hipaa_compliance_array)
    dups(mail)

    if trace_array_lists_two:
        print("hipaa_compliance: " + str(final_hipaa_compliance_array))
        print("expanded_hipaa_compliance: " + str(final_expanded_hipaa_compliance_array))
        print("mail: " + str(mail))

    # update each file
    hipaa_compliance_array['enabled_orgs'] = final_hipaa_compliance_array
    writeJson(repo+"features/hipaa_compliance", hipaa_compliance_array)
    expanded_hipaa_compliance_array['enabled_orgs'] = final_expanded_hipaa_compliance_array
    writeJson(repo+"features/expanded_hipaa_compliance", expanded_hipaa_compliance_array)
    writeMailGun(repo+"consul_config/mail.ini", mail)



if __name__=="__main__":
    main()




