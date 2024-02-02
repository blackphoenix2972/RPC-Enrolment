import xmlrpc.client


unit_scores = [{}]

def send_data_to_server(person_id, first_name, last_name, email):
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        user_exists_in_database = proxy.test(person_id, first_name, last_name, email)
      
        
        if (user_exists_in_database == True):
            print("\nUser found!\n")
            print(proxy.evaluate_eligibility())
        else:
            print("\nUser not found\n")

def send_data_to_server_no(data, person_id):
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        x = proxy.data(person_id, data)
 
        # proxy.data( person_id,data)
        # count = proxy.dictionary_list_length()
        print(proxy.evaluate_eligibility())
        # return count
def get_non_oust_student_data():
        global unit_scores
        Reset_Unit_Scores()
        try:
            person_id = int(input("\nEnter your Person ID: "))
        except ValueError:
            print("Person ID must be a number")
            return
            

        while True:
            unit_code = input("Enter a unit code (enter 'stop' to finish): ")
            if unit_code.lower() == 'stop':
                if(not unit_scores):
                    print("\nYou need to add a course...\n")
                    continue
                
                res = send_data_to_server_no(data=unit_scores, person_id=person_id)
                break
            if (len(unit_code) != 0):
                try:

                    mark = float(input(f"Enter the mark for unit {unit_code}: "))
                    
                    if mark < 0 or mark > 100:
                        print("\nInvalid mark. Mark must be between 0 and 100. Did not add...\n")
                    else:
                        print(f'\n<{unit_code}, {mark}> => Added\n')
                        unit_scores.append({'unit_code': unit_code, 'mark': mark})
                        
                except ValueError:
                    print("\nMarks should be an integer or float\nMark not added.\n")
            else:
                print("\nError: unit code cannot be empty\n")
        # print(unit_scores)
        
       


def Reset_Unit_Scores():
    global unit_scores
    unit_scores = []

def main():
    keep_running = True
    while keep_running:
        user_input = ""
        person_id = ""
        last_name = ""
        email = ""
        print("\nAre you an OUST student? [Yes / No / Exit]")
        user_input = input("> ")
        if (user_input.lower() == "yes"):
            print("\nInformation: ")
            person_id = input("\nEnter Person ID: ") # check 8 digits
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("OUST Email Address: ")
            send_data_to_server(person_id=person_id, first_name=first_name, last_name=last_name, email=email)


        elif(user_input.lower() =="no"):
            get_non_oust_student_data()
        elif(user_input.lower() =="exit"):
            print("\nExiting the program...\n")
            keep_running = False

        else:
            print("\nError! invalid input detected! Please select [Yes / No]\n")

if __name__ == "__main__":
    main()
