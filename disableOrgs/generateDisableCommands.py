#!/usr/bin/python3
import re

def get_user_input(String):
    
    val = input("Enter " + String +":")
    return val

def createFileArray(file, trace=False):
    file_array=[]

    with open(file) as f:
        for line in f:
            file_array.append(line)

    if trace:
        for l in file_array:
            print(l)

    return file_array

def cleanUpMailIniArray(ary):
    mail_array=[]

    for i in ary:
        num = re.findall(r'\d+', i)
        if len(num) > 0:
            mail_array.append(num[0])
    return mail_array


def main():
    adminEmail = "team-advocacy@datadoghq.com"
    agentEmail = "zachary.stall@datadoghq.com"
    planType = "Student"
    orgName = "Ara Pulido Backpack"
    zdTicket = "https://datadog.zendesk.com/agent/tickets/1027391"

    orgArray = createFileArray('disableOrgsList')
    org_id = cleanUpMailIniArray(orgArray)

    for id in org_id:
        print('dogq org disable ' + str(id) + '--reason "' +zdTicket +'" --email "' +agentEmail+ '" --org_name "'+orgName+'" --admin_email "'+adminEmail+'" --plan_name "'+planType+'"')



if __name__=="__main__":
    main()