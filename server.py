from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class AverageServer:
    def data(self,person_id, data):
        self.data = data
        self.person_id = person_id
        
        return data

    def calculate_average(self):
        total = 0
        marks_list = []
        
        for key in self.data:
            marks_list.append(int(key['mark']))
            total+=int(key['mark'])
        self.marks_list = marks_list
        average = total / len(marks_list)
        return average

    def dictionary_list_length(self):
        count = 0
        for key in self.data:
            count+=1
        return count
    
    def calculate_best_nth_average(self, nth):
        sorted_marks_list_ascending = sorted(self.marks_list)
        print(sorted_marks_list_ascending)
        count = 0
        total = 0
        if (len(self.marks_list) >= nth):
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
        course_average = self.calculate_average()
        
        length_of_dictionary_list = self.dictionary_list_length()
      
        person_id = self.person_id
        best_8th_average = self.calculate_best_nth_average(8)
        
        units_failed_count = self.count_unit_fails()


        if length_of_dictionary_list <= 15:
            return f"\n<{person_id}>, <{course_average}>, completed less than 16 units! DOES NOT QUALIFY FOR HONORS STUDY!"

        if units_failed_count >= 6:
            return f"\n{person_id}, {course_average}, with 6 or more Fails! DOES NOT QUALIFY FOR HONORS STUDY!"

        if course_average >= 70:
            return f"\n{person_id}, {course_average}, QUALIFIES FOR HONOURS STUDY!"

        if (course_average < 70 and course_average >= 65) and best_8th_average >= 80:
            return f"\n{person_id}, {course_average}, {best_8th_average}, QUALIFIES FOR HONOURS STUDY!"

        if(course_average < 70 and course_average >= 65) and best_8th_average < 80:
            return f"\n{person_id}, {course_average}, {best_8th_average}, MAY HAVE GOOD CHANCE! Need further assessment."

        if (course_average < 65 and course_average >= 60) and best_8th_average >= 80:
            return f"\n{person_id}, {course_average}, {best_8th_average}, MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s permission."

        return f"\n{person_id}, {course_average}, DOES NOT QUALIFY FOR HONORS STUDY!"   
def run_server():
    server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)
    avg_server = AverageServer()
    server.register_function(avg_server.data, "data")
    server.register_function(avg_server.dictionary_list_length, "dictionary_list_length")
    server.register_function(avg_server.evaluate_eligibility, "evaluate_eligibility")

    print("Server listening on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
