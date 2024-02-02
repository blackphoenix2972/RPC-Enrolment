from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from DatabaseConnect import create_connection

class ServerRPC:
    def test(self, person_id, first_name, last_name, email):
        connection = create_connection()
        user_exists_in_database = False
        if connection:
            try:
                cursor = connection.cursor()
                
                
                cursor.execute("SELECT * FROM dbo.OUST_Student WHERE Person_ID = ? AND First_Name=? AND Last_Name=? AND OUST_Email=?", (int(person_id), first_name.lower(), last_name.lower(), email.lower()))
                rows = cursor.fetchall()
                # Record found in database
                if (len(rows) > 0):
                    user_exists_in_database = True
                    
                
                if (user_exists_in_database == True):

                    cursor.execute("SELECT Course_Code, Marks FROM dbo.OUST_Student_Course WHERE Person_ID = ?", (person_id))
                    rows = cursor.fetchall()
                    self.data = []
                    for row in rows:
                        
                        print("<"+ str(row[0]) + ", " + str(row[1]) + ">")
                        
                        self.data.append({"course_code": row[0], "mark": row[1]})
                        for x in self.data:
                            print(x)
                        self.person_id = person_id
                        
                    

                        

                # Close the cursor
                cursor.close()
                return user_exists_in_database

            except Exception as e:
                return f"Error: {str(e)}"
            finally:
                 connection.close()
    def data(self,person_id, data):
        self.data = data
        self.person_id = person_id
        
        return data

    def calculate_average(self, dictionary_list):
        self.marks_list = []
        total = 0
       
        for key in dictionary_list:
            self.marks_list.append(int(key['mark']))
            total+=int(key['mark'])

        # Return the average
        return round((total / len(self.marks_list)),2)

    def dictionary_list_length(self, dictionary_list):
        return len(dictionary_list)
    
    def calculate_best_nth_average(self, nth):
        count = 0
        total = 0

        length_of_marks_list = len(self.marks_list)
        sorted_marks_list_ascending = sorted(self.marks_list)
        print(sorted_marks_list_ascending)
       
        if (length_of_marks_list >= nth):
            for x in sorted_marks_list_ascending:
                if (count == nth):
                    break
                count+=1
                total+=x
            return total / nth

    def count_unit_fails(self):
        units_failed = 0
   
        for x in self.marks_list:
            if (x < 50):
                    units_failed+=1
        return units_failed
            
        
    def evaluate_eligibility(self):
        course_average = self.calculate_average(dictionary_list=self.data)
        
        length_of_dictionary_list = self.dictionary_list_length(dictionary_list=self.data)
     
        person_id = self.person_id
        best_8th_average = self.calculate_best_nth_average(nth=8)
        
        units_failed_count = self.count_unit_fails()


        if length_of_dictionary_list <= 15:
            return f"\n<{person_id}>, <{course_average}>, completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!\n"

        if units_failed_count >= 6:
            return f"\n<{person_id}>, <{course_average}>, with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!\n"

        if course_average >= 70:
            return f"\n<{person_id}>, <{course_average}>, QUALIFIES FOR HONOURS STUDY!\n"

        if (course_average < 70 and course_average >= 65) and best_8th_average >= 80:
            return f"\n<{person_id}>, <{course_average}>, <{best_8th_average}>, QUALIFIES FOR HONOURS STUDY!\n"

        if(course_average < 70 and course_average >= 65) and best_8th_average < 80:
            return f"\n<{person_id}>, <{course_average}>, <{best_8th_average}>, MAY HAVE GOOD CHANCE! Need further assessment.\n"

        if (course_average < 65 and course_average >= 60) and best_8th_average >= 80:
            return f"\n<{person_id}>, <{course_average}>, <{best_8th_average}>, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission.\n"

        return f"\n<{person_id}>, <{course_average}>, DOES NOT QUALIFY FOR HONORS STUDY!\n" 
      
def run_server():
    server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)
    avg_server = ServerRPC()
    server.register_function(avg_server.test, "test")

    server.register_function(avg_server.data, "data")
    server.register_function(avg_server.dictionary_list_length, "dictionary_list_length")
    server.register_function(avg_server.evaluate_eligibility, "evaluate_eligibility")
    print("Server listening on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
