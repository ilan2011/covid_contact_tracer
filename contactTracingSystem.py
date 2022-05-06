#Author: Ilan Breines 261036901

from student import Student
from contactTracker import ContactTracker

def load_file(file_name):
    """(str)-> Nonetype
takes a string parameter file_name, opens the file with the given file name and returns
its content as a string. If any error occurs when trying to read the file after the file
has been opened, then the function should close the file before the exception is raised.
If the file didn’t open successfully, do not handle that case in this function.
"""
    fobj = open(file_name, "r") 
    
    try:
        file_content = fobj.read() 
        return file_content
    
    except:
        print("file with name "+file_name+" could not be read.")
        
    finally:
        fobj.close()


def JSON_to_students(data):
    """(str)-> list(Student)
takes a string in JSON format containing students’ list (in the format that is indicated
in cases.csv) and returns a list of Student objects. The function assumes that the
parameter is a valid JSON object.

>>> data = load_file("all_students.json")
>>> print(JSON_to_students(data))
[Bob (260808934), Paul (260840155), Mark (260248711), Carol (260996175), Leanne (260476020),
Will (260561504), Farley (260675874), Sarai (260758421), Larry (260386543),
Philip (260212160), Zach (260970944)]

>>> data = load_file("all_students.json")
>>> print(JSON_to_students(data))
[Tayvon (260987654), Jarrad (260345812), Paid (260911111),
Philip (260212160), Sarai (260758421)]

>>> data = load_file("all_students.json")
>>> print(JSON_to_students(data))
[Talen (260987654), Polly (260981275)]
"""
    json_strings = []
    json_string = ""
    is_json_string = False
    
    for index, char in enumerate(data):
    #new student is indicated by { and }, also able to ignore potential formatting issues    
        if char == "{":
            is_json_string = True
        
        if data[index-1] == "}":
            is_json_string = False
            
            if len(json_string) != 0:
                json_strings.append(json_string)
                json_string = ""
        
        if is_json_string:
            json_string+=char
    
    students = []
    
    for json_string in json_strings:
        
        student_obj = Student.from_JSON(json_string)
        students.append(student_obj)
    
    return students




def csv_to_dictionary(data):
    """(string)-> dictionary
takes a string in CSV format and returns a dictionary where the keys are the sick students’
ids, and for each sick student the value is the list of student IDs that the sick student
had contact with.

>>> data = load_file("cases.csv")
>>> print(csv_to_dictionary(data))
{'260386543': ['260996175', '260248711', '260476020', '260561504'],
'260248711': ['260212160', '260970944'],
'260840155': ['260970944'],
'260561504': ['260476020', '260248711'], '260970944': ['260212160']}

>>> data = load_file("cases.csv")
>>> print(csv_to_dictionary(data))
{'260808934': ['260840155', '260248711', '260996175', '260476020', '260561504'],
'260996175': ['260248711', '260476020'],
'260675874': ['260840155'],
'260476020': ['260758421'],
'260386543': ['260996175', '260248711', '260476020', '260561504'],
'260248711': ['260212160', '260970944'],
'260840155': ['260970944'],
'260561504': ['260476020', '260248711'], '260970944': ['260212160']}

>>> data = load_file("cases.csv")
>>> print(csv_to_dictionary(data))
{'260675874': ['260840155'],
'260476020': ['260758421'],
'260386543': ['260996175', '260248711', '260476020', '260561504'],
'260248711': ['260212160', '260970944'],
'260840155': ['260970944']}

"""
    split_by_line = data.split("\n")
    contact_lists = []
    #split by each line to isolate indivudial sick person and their contacts
    for line in split_by_line:
        line = line.split(",")
        contact_lists.append(line)
    #split at the comma to get each student id in the contact list
    for contact_list in contact_lists:
        
        for index, contact in enumerate(contact_list):
            contact_list.remove(contact)
            contact_list.insert(index,contact.strip())
            #removes lingering spaces
    
    dictionary_of_contacts = {}
    for contact_list in contact_lists:
        sick_student = contact_list.pop(0) #this allows function to use sick student as key
        dictionary_of_contacts[sick_student]=contact_list
    
    return dictionary_of_contacts


def build_report(contact_tracker):
    """(ContactTracker)-> string
takes an object of type ContactTracker, constructs and returns a string
that is a contract tracing report by calling functions from Contact Tracker
module.
"""
    
    report = ""
    
    contact_records = "Contact Records:"
    contacts = contact_tracker.contact_objects()
    for contact in contacts:
        contact_record__string = "\n\t"+str(contact)+" had contact with "
        contacted = contact_tracker.get_contacts_by_student_id(contact.student_id)
        
        if len(contacts) == 0:
            contact_record__string+="none"
        else:
            for index, student in enumerate(contacted):
                
                if index == 0:
                    contact_record__string+=str(student)
                
                else:
                    contact_record__string+=", "+str(student)
            
            contact_records+= contact_record__string
    
    report+= contact_records+"\n\n"
    
    patient_zeros = contact_tracker.patient_zeros()
    patient_zeroes_line = generate_line_for_report("Patient Zero(s): ", patient_zeros)
    report+=patient_zeroes_line+"\n"
    
    potential_sick_students = contact_tracker.potential_sick_students()
    prefix = "Potential sick students: "
    potential_sick_students_line = generate_line_for_report(prefix, potential_sick_students)
    report+=potential_sick_students_line+"\n"
    
    sick_from_other_student = contact_tracker.sick_from_another_student()
    prefix = "Sick students who got infected from another student: "
    sick_from_others_line= generate_line_for_report(prefix, sick_from_other_student)
    report+=sick_from_others_line+"\n"
    
    most_viral_students = contact_tracker.most_viral_students()
    prefix = "Most viral students: "
    most_viral_students_line = generate_line_for_report(prefix,most_viral_students)
    report+=most_viral_students_line+"\n"
    
    most_contacted_students = contact_tracker.most_contacted_student()
    prefix
    most_contacted_students_line = generate_line_for_report(prefix,most_contacted_students)
    report+=most_contacted_students_line+"\n"
    
    ultra_spreaders = contact_tracker.ultra_spreaders()
    ultra_spreaders_line = generate_line_for_report("Ultra spreaders: ",ultra_spreaders)
    report+=ultra_spreaders_line+"\n"
    
    non_spreaders = contact_tracker.non_spreaders()
    non_spreaders_line = generate_line_for_report("Non-spreaders: ",non_spreaders)
    report+=non_spreaders_line+"\n"
    
    min_distances_info='\nFor bonus:\nMinimum distances of students from patient zeros:'
    
    for index, student in enumerate(contact_tracker.students):
        min_dist = contact_tracker.min_distance_from_patient_zeros(student.student_id)
        if index != len(contact_tracker.students)-1:
            min_distances_info+="\n\t"+str(student)+": "+str(min_dist)+","
        else:
            min_distances_info+="\n\t"+str(student)+": "+str(min_dist)
    
    report+=min_distances_info
    
    return report

def generate_line_for_report(line_prefix, list_of_people):
    """(str,list)-> string
takes a sentence prefix such as "Potential sick students: " and a list of people
and constructs and returns a string for the tracing report using the inputted
information

>>> most_contacted_students = contact_tracker.most_contacted_student()
>>> generate_line_for_report("Most contacted students: ",most_contacted_students)
Most contacted students: Leanne (260476020), Mark (260248711)

>>> ultra_spreaders = contact_tracker.ultra_spreaders()
>>> generate_line_for_report("Ultra spreaders: ",ultra_spreaders)
Ultra spreaders: Leanne (260476020), Zach (260970944)

>>> most_viral_students = contact_tracker.most_viral_students()
>>> mvs_line = generate_line_for_report("Most viral students: ",most_viral_students)
Most viral students: Bob (260808934)
"""
    prefix = line_prefix
    
    if len(list_of_people) == 0:
        prefix += "none"
    
    else:
        for index, person in enumerate(list_of_people):
            
            if index == 0:
                prefix+=str(person) #no comma in front of first person
            
            else:
                prefix+=", "+str(person) 
    
    return prefix
            

def write_in_file(file_name,text):
    """(str,str)-> Nonetype
takes two parameters – a string file_name and a string text, and does not return anything.
The function writes the value of text in the specified file. If any error occurs when trying
to write in the file after the file has been opened successfully, then the function closes
the file before the exception is raised.
"""
    fobj = open(file_name, "w") 
    
    try:
        fobj.write(text) 
    
    except:
        print("there was a problem writing to file with name "+file_name)
    
    finally:
        fobj.close()

    
           
def main():
    """()-> Nonetype
takes no parameters and returns nothing. The function takes the data from the initial files,
creates an instance of ContactTracker class, builds the report and writes the final report
in a file called contact_tracing_report.txt. Finally, if any of the initial files
all_students.json or cases.csv is not found, program catches error and prints message. 
"""
    try:
        file_name="all_students.json"
        student_data = load_file(file_name)
        students = JSON_to_students(student_data)
        
        file_name="cases.csv"
        cases_data = load_file(file_name)
        cases = csv_to_dictionary(cases_data)
        
        i=0
    
    except FileNotFoundError:
        
        print("Sorry, the file "+file_name+" could not be found.")
        i=1
    
    if i==0:
        
        contact_tracker = ContactTracker(students,cases)
        report = build_report(contact_tracker)
        write_in_file("contact_tracing_report.txt",report)
    
             
main()