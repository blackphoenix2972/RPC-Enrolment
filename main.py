import xmlrpc.client


unit_scores = [{}]

def send_data_to_server(data, person_id):
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        proxy.data( person_id,data)
        count = proxy.dictionary_list_length()
        print(proxy.evaluate_eligibility())
        return count
def get_non_oust_student_data():
        global unit_scores
        Reset_Unit_Scores()
        person_id = input("Enter your Person ID: ")
       
        while True:
            unit_code = input("Enter a unit code (enter 'stop' to finish): ")
            if unit_code.lower() == 'stop':
                break
            
            mark = input(f"Enter the mark for unit {unit_code}: ")
            unit_scores.append({'unit_code': unit_code, 'mark': mark})
        print(unit_scores)
        res = send_data_to_server(unit_scores, person_id=person_id)
        print(res)

        # for key in unit_scores:
        #     print(key['mark'])
       

def Reset_Unit_Scores():
    global unit_scores
    unit_scores = []

def main():
    print("Are you an OUST student?")
    x = input()
    if (x == "y"):
        print("\nInformation: ")
        input("\nEnter Person ID: ") # check 8 digits
        input("Enter First Name: ")
        input("Enter Last Name: ")
        input("OUST Email Address: ")
    elif(x =="n"):
        get_non_oust_student_data()



    # lyst = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, -1]
    # result = send_data_to_server(lyst)
    # print("The average value is:", result)

    # lyst1 = []
    # while True:
    #     v = input("Please enter an integer as a unit mark (enter -1 to stop): ")
    #     x = int(v)
    #     if x != -1:
    #         lyst1.append(x)
    #     else:
    #         lyst1.append(-1)
    #         break

    # result = send_data_to_server(lyst1)
    # print("The average value is:", result)

if __name__ == "__main__":
    main()
