try:
    from Kernel import thestart, Debugstat, findingtheplanning, findtheplanningdate, findingseparations, Enclave_completing, cashe_list, match
    import random
    import CommonUtil
    if Debugstat:
        print("* PlanCrafting successfully imported")
except:
    ImportError

#Processing the text to be more clean
def Apllicator(User_message): 
    global start_index, end_index, message
                
    message = User_message           
    start_index = findingtheplanning.values.start()
    end_index = (findtheplanningdate.values.end() if findtheplanningdate["date"] else find_engine(User_message))
    print(User_message[start_index:end_index])