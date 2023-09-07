import json

def requires_user_input(field):
    return field["required"] and not field["has_default_value"] and field["key"] not in {"project", "issuetype", "summary", "description", "reporter"}


def main():

    print("Output from jira api for DEV")
    with open('dev.json') as f:
        d = json.load(f)
    
    for field in d["fields"]:
        if requires_user_input(field):
            print(field)
            print("is required:")
            print("Checking required: " + str(field["required"]) + " Checking default: " + str(field["has_default_value"]) +" and field['key']: " + str(field["key"]) )
            print(requires_user_input(field))
            print("=================")


    print("Output from jira api for PSUPDEV")
    with open('psupdev.json') as f:
        d = json.load(f)
    
    for field in d["fields"]:
        if requires_user_input(field):
            print(field)
            print("is required:")
            print("Checking required: " + str(field["required"]) + " and field['key']: " + str(field["key"]) )
            print(requires_user_input(field))
            print("=================") 


if __name__=="__main__":
    main()