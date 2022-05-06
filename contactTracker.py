
from student import Student


class ContactTracker:
    """
class reperesenting ContactTracker which is used to trace covid cases.
"""
    students = []

    def __init__(self,students, cases_with_contacts):     
        """(list,dict)-> ContactTracker
the constructor for the class, takes two inputs to initiate the attributes of the class
a list of Student objs and a dictionary to initiate the instance attribute cases_with_contacts
The attribute students is set only once for the entire class of ContactTracker. The constructor
also checks that all the student IDs appearing in cases_with_contacts can be found in the
registered students list. If such a student ID cannot be found, for example '260245896',
then ValueError with a message 'A student with id 260245896 either doesn't exist or is not
reported as sick.' Finally, the initializations of the attribute cases_with_contacts
are done by deep copying.

>>>students_list = [{"id": "260808934", "name": "Bob"},{"id": "260840155", "name": "Paul"},
{"id": "260248711", "name": "Mark"}, {"id": "260996175", "name": "Carol"},
{"id": "260476020", "name": "Leanne"},{"id": "260561504", "name": "Will"},
{"id": "260675874", "name": "Farley"},{"id": "260758421", "name": "Sarai"},
{"id": "260386543", "name": "Larry"},{"id": "260212160", "name": "Philip"},
{"id": "260970944", "name": "Zach"}]
>>> cases_dict ={'260808934': ['260840155', '260248711', '260996175', '260476020', '260561504'],
          '260996175': ['260248711', '260476020'],
          '260675874': ['260840155'],
          '260476020': ['260758421'],
          '260386543': ['260996175', '260248711', '260476020', '260561504'],
          '260248711': ['260212160', '260970944'],
          '260840155': ['260970944'],
          '260561504': ['260476020', '260248711'],
          '260970944': ['260212160']}
>>> contact_tracker = ContactTracker(students_list,cases_dict)
>>> type(contact_tracker)
<class '__main__.ContactTracker'>

>>> students_list = [{"id": "260808934", "name": "Bob"},{"id": "260840155", "name": "Paul"}]
>>> cases_dict ={'260808934': ["260840155"]}
>>> contact_tracker = ContactTracker(students_list,cases_dict)
>>> type(contact_tracker)
<class '__main__.ContactTracker'>

>>> students_list = [{"id": "260808934", "name": "Bob"},{"id": "260840155", "name": "Paul"}]
>>> cases_dict ={'26011111': ["260840155"]}
>>> contact_tracker = ContactTracker(students_list,cases_dict)
Traceback (most recent call last):
ValueError: A student with id 26011111 either doesn't exist or is not reported as sick.
"""
        if len(ContactTracker.students) == 0:  #only sets class attribute students once
            ContactTracker.students = students
        
        self.cases_with_contacts = self.deep_copy_cases_dict(cases_with_contacts) 
                                                        #deep copy dictionary
        student_ids = []
        for student in ContactTracker.students:  
            student_ids.append(student.student_id)
        
        for key in self.cases_with_contacts:#block of code validates student id 
            
            if key not in student_ids:
                error = " either doesn't exist or is not reported as sick."
                raise ValueError("A student with id "+key+ error)
            
            for value in self.cases_with_contacts[key]:
                
                if value not in student_ids:
                    error = " either doesn't exist or is not reported as sick."
                    raise ValueError("A student with id "+key+ error)
        
    def get_contacts_by_student_id(self,student_id):
        """(str)-> list
takes a student_id of a sick student as an input and returns the list of Student objects
that the sick student has been in contact with. If such a student_id cannot be found,
value error with messagee 'A student with id *student_id* either doesn't exist
or is not reported as sick.'

>>> students_list = contact_tracker.get_contacts_by_student_id('260996175')
>>> print(students_list)
[Mark (260248711), Leanne (260476020)]

>>> students_list = contact_tracker.get_contacts_by_student_id('260675874')
>>> print(students_list)
[Paul (260840155)]

>>> students_list = contact_tracker.get_contacts_by_student_id('260111111')
Traceback (most recent call last):
ValueError: A student with id 260111111 either doesn't exist or is not reported as sick.
"""
        contacted_student_objs=[]
    
        student_ids=[]
        for student in self.students:
            student_ids.append(student.student_id)
            
        if student_id not in student_ids: #makes sure student id is in student data set
            error = " either doesn't exist or is not reported as sick."
            raise ValueError("A student with id "+student_id+ error)
            
        contacted_students=self.cases_with_contacts[student_id]
        
        for student in self.students: #adds student if they are in contacted student list
            if student.student_id in contacted_students:
                contacted_student_objs.append(student)
        
        return contacted_student_objs
    
    def get_all_contacts(self):
        """()-> dict
takes no parameters and returns a dictionary where the keys are the student IDs
of sick students. For each sick student the value in the dictionary is the list
of Student objects corresponding to the students that the sick student had contact with.

>>> print(contact_tracker.get_all_contacts())
{'260808934': [Paul (260840155), Mark (260248711), Carol (260996175), Leanne (260476020),
Will (260561504)],
'260996175': [Mark (260248711), Leanne (260476020)],
'260675874': [Paul (260840155)],
'260476020': [Sarai (260758421)],
'260386543': [Carol (260996175), Mark (260248711), Leanne (260476020), Will (260561504)],
'260248711': [Philip (260212160), Zach (260970944)],
'260840155': [Zach (260970944)],
'260561504': [Leanne (260476020), Mark (260248711)],
'260970944': [Philip (260212160)]}

>>> print(contact_tracker.get_all_contacts())
{'260123456': [Ilan (260098765), Tamar (260444444)]}

>>> print(contact_tracker.get_all_contacts())
{'260123456': [Ilan (260098765), Tamar (260444444)],
'260666665': [Terry (260121212), Jake (260989898), Jax (260323295)]}
"""
        all_contacts = {}
        
        for sick_student in self.cases_with_contacts.keys():
            contacts = self.get_contacts_by_student_id(sick_student)
            all_contacts[sick_student] = contacts
        
        return all_contacts
    
    def patient_zeros(self):
        """()-> list
takes no parameters and returns a list of sick students (Student objects) who are the possible
patient zero(s). In this setting, we define the patient zero to be a sick student who didn’t
contract the virus from any McGill student, meaning the student didn’t appear in any other
sick student’s contact list. Assume there is always a patient zero in the dataset.

>>> print(contact_tracker.patient_zeros())
[Bob (260808934), Farley (260675874), Larry (260386543)]

>>> print(contact_tracker.patient_zeros())
[Talen (260987654), Polly (260981275)]

>>> print(contact_tracker.patient_zeros())
[Draymond (260854712)]
"""
        patient_zeros = []
        sick_students = []
        
        for student in self.students:
            if student.student_id in self.cases_with_contacts.keys():
                sick_students.append(student)
        
        for sick_student in sick_students:
            patient_zero=True
            
            for key in self.cases_with_contacts:
                
                if sick_student.student_id in self.cases_with_contacts[key]:
                    patient_zero=False
                    break
            
            if patient_zero:
                patient_zeros.append(sick_student)
        
        return patient_zeros
    
    def potential_sick_students(self):
        """()-> list
takes no parameters and returns a list of students (Student objects) who are not reported to be
sick, but might be sick because they appear in a sick student’s contact list. If there aren’t
any such students, the function should return an empty list.

>>> print(contact_tracker.potential_sick_students())
[Philip (260212160), Sarai (260758421)]

>>> print(contact_tracker.potential_sick_students())
[Trayvon (260987654)]

>>> print(contact_tracker.potential_sick_students())
[Tayvon (260987654), Jarrad (260345812), Paid (260911111)]
"""
        potential_sick_students = []
        
        for student in self.students:
            potentially_sick = False
            
            #student is potentially sick if they are a dict value but not dict key 
            for key in self.cases_with_contacts:
                
                if student.student_id in self.cases_with_contacts[key]:
                    potentially_sick = True 
            
            if student.student_id in self.cases_with_contacts.keys():
                potentially_sick = False
            
            if potentially_sick:
                potential_sick_students.append(student)
            
        return potential_sick_students
    
    def sick_from_another_student(self):
        """()-> list
sick_from_another_student: takes no parameters and returns a list of sick students
(Student objects) who got sick from another student, i.e. they appeared in a
contact list of a sick student (that’s probably how they got sick). In other words,
these are the sick students in the contact list who are neither patient zero(s)
nor potentially sick. If there aren’t any, the function should return an empty list.

>>> print(contact_tracker.sick_from_another_student())
[Carol (260996175), Leanne (260476020), Mark (260248711), Paul (260840155), Will (260561504),
Zach (260970944)]

>>> print(contact_tracker.sick_from_another_student())
[Tayvon (260987654), Jarrad (260345812), Paid (260911111), Philip (260212160),
Sarai (260758421)]

>>> print(contact_tracker.sick_from_another_student())
[Ty (260987654), TyTy (260345812), Paidy (260911111), Geogino (260987654), Sarity (260123455),
Joshy (260987456)]
"""
        sick_from_others = []
        patient_zeros = self.patient_zeros()
        potential_sick = self.potential_sick_students()
        all_contacts = self.get_all_contacts()
        
        #looking for sick students who are not in patient_zeros or potential_sick
        for student in self.students:
            
            for key in all_contacts:
                
                if student in all_contacts[key]:
                    
                    if student not in patient_zeros and student not in potential_sick:
                        
                        if student not in sick_from_others:
                            sick_from_others.append(student)

        return sick_from_others

    def most_viral_students(self):
        """()-> list
takes no parameters and returns a list of the most viral student(s) (Student objects).
The most viral student is the student who contacted the largest number of other students,
meaning the student who had the longest list of contacts.

>>> print(contact_tracker.most_viral_students())
[Bob (260808934)]

>>> print(contact_tracker.most_viral_students())
[Jaytan (260111234)]

>>> print(contact_tracker.most_viral_students())
[Trayvon (260987654)]
"""
        most_viral_students = []
        highest_num_contacted = 0
        
        all_contacts = self.get_all_contacts()
        
        for spreader in all_contacts.keys():
            contacts = self.get_contacts_by_student_id(spreader)
            
            if len(contacts) > highest_num_contacted:
                highest_num_contacted = len(contacts)
        
        for student in self.students:
            
            if student.student_id in all_contacts.keys():
        #checks if length of students contact list matches max value
                contacts_by_student = self.get_contacts_by_student_id(student.student_id)
                if len(contacts_by_student) == highest_num_contacted:
                    most_viral_students.append(student)
        
        return most_viral_students
    
    def most_contacted_student(self):
        """()-> list
takes no parameters and returns a list of the most contacted student(s) (Student objects).
The most contacted student is the student who is not reported as sick, but has been in
contact with the most amount of sick students, so most likely the student is also sick
and thus should contacted by contact tracers. 

>>> print(contact_tracker.most_contacted_student())
[Philip (260212160)]

>>> print(contact_tracker.most_contacted_student())
[Jarrad (260345812)]

>>> print(contact_tracker.most_contacted_student())
[]
"""
        most_contacted_students = []
        highest_num_contacted = 0
        students_and_times_contacted = {}
        all_contacts = self.get_all_contacts()
        students_contacted = []
        
        for student in self.students:
            #student cannot be counted if they are reported as sick
            if student not in self.contact_objects(): 
                times_contacted = 0
                
                for key in all_contacts:
                    
                    if student in all_contacts[key]:
                        times_contacted+=1
                
                students_and_times_contacted[student.student_id]=times_contacted
                students_contacted.append(student)
                
                if times_contacted > highest_num_contacted:
                    highest_num_contacted = times_contacted
        
        for student in students_contacted:
            
            if students_and_times_contacted[student.student_id] == highest_num_contacted:
                most_contacted_students.append(student)
        
        return most_contacted_students
            
    def ultra_spreaders(self):
        """()-> list
takes no parameters and returns the list of spreader students (Student objects).
An ultra spreader is a sick student who only has had contact with potentially
sick students (no student in their contact list is sick yet). If there aren’t
any, the function should return an empty list.

>>> print(contact_tracker.ultra_spreaders())
[Leanne (260476020), Zach (260970944)]

>>> print(contact_tracker.ultra_spreaders())
[Tamar (260458923), Ilan (260999888)]

>>> print(contact_tracker.ultra_spreaders())
[]
"""
        ultra_spreader_strings = []
        all_contacts = self.get_all_contacts()
        potential_sick_students = self.potential_sick_students()
        
        for spreader in all_contacts:
            ultra_spreader = True
            
            for contact in all_contacts[spreader]:
                
                if contact not in potential_sick_students:
                    ultra_spreader = False
            if ultra_spreader:
                ultra_spreader_strings.append(spreader)
        
        contact_objects = self.contact_objects()
        ultra_spreaders = []
        
        for contact in contact_objects:
            
            if contact.student_id in ultra_spreader_strings:
                ultra_spreaders.append(contact)
        
        return ultra_spreaders
            
    
    def contact_objects(self):#helper function
        """()-> list
this helper function takes no inputs and returns a list of first contacts (sick students)
from cases_with_contacts.

>>> print(contact_tracker.contact_objects())
[Bob (260808934), Paul (260840155), Mark (260248711), Carol (260996175), Leanne (260476020),
Will (260561504), Farley (260675874), Larry (260386543), Zach (260970944)]

>>> print(contact_tracker.contact_objects())
[Tayvon (260987654), Jarrad (260345812), Paid (260911111), Philip (260212160), Sarai (260758421)]

>>> print(contact_tracker.contact_objects())
[Ty (260987654), TyTy (260345812), Paidy (260911111), Geogino (260987654), Sarity (260123455),
Joshy (260987456)
"""
        contacts = []
        for student in self.students:
            
            if student.student_id in self.cases_with_contacts.keys():
                contacts.append(student)
        
        return contacts
            
    def non_spreaders(self):
        """()-> list
 takes no parameters and returns the list of non-spreader students (Student objects).
 A non-spreader is a sick student that had contact only with other sick students.
 If there aren’t any, the function returns an empty list.
 
>>> print(contact_tracker.non_spreaders())
[Bob (260808934), Carol (260996175), Farley (260675874), Larry (260386543),
Paul (260840155), Will (260561504)]

>>> print(contact_tracker.non_spreaders())
[]

>>> print(contact_tracker.non_spreaders())
[Tayvon (260987654), Jarrad (260345812), Paid (260911111)]
"""
        non_spreader_strings = []
        all_contacts = self.get_all_contacts()
        students_sick_from_others = self.sick_from_another_student()
        
        for spreader in all_contacts:
            non_spreader = True
            
            for contact in all_contacts[spreader]:
                
                if contact not in students_sick_from_others:
                    non_spreader = False
            
            if non_spreader:
                non_spreader_strings.append(spreader)
        
        contact_objects = self.contact_objects()
        non_spreaders = []
        
        for contact in contact_objects:
            
            if contact.student_id in non_spreader_strings:
                non_spreaders.append(contact)
        
        return non_spreaders
    
    
    @staticmethod
    def deep_copy_cases_dict(dictionary):
        """(dict)-> dictionary
takes a dictionary in format of cases_with_copies and
returns a deep_copied dictionary.

>>> dict= {"123": ["1", "3", "5"]}
>>> deep_copy_cases_dict(dict)
{"123": [1, 3, 5]}

>>> dict = {'260808934': ['260840155', '260248711', '260996175', '260476020', '260561504'],
          '260996175': ['260248711', '260476020'],
          '260675874': ['260840155'],
          '260476020': ['260758421'],
          '260386543': ['260996175', '260248711', '260476020', '260561504'],
          '260248711': ['260212160', '260970944'],
          '260840155': ['260970944'],
          '260561504': ['260476020', '260248711'],
          '260970944': ['260212160']}
>>> deep_copy_cases_dict(dict)
{'260808934': ['260840155', '260248711', '260996175', '260476020', '260561504'],
          '260996175': ['260248711', '260476020'],
          '260675874': ['260840155'],
          '260476020': ['260758421'],
          '260386543': ['260996175', '260248711', '260476020', '260561504'],
          '260248711': ['260212160', '260970944'],
          '260840155': ['260970944'],
          '260561504': ['260476020', '260248711'],
          '260970944': ['260212160']}
          
>>> dict= {"123": ["1", "3", "5"], "345" : ["1", "6", "23323"]}
>>> deep_copy_cases_dict(dict)
dict= {"123": ["1", "3", "5"], "345" : ["1", "6", "23323"]}
"""
        copied_dict = {}
        
        for key in dictionary:
            copied_dict[key[:]]= dictionary[key][:]
        
        return copied_dict
    
    def min_distance_from_patient_zeros(self,student_id):
        """(str)_> int
takes a student_id of a student as an input and returns an int corresponding to the students
minimum distance from a patient zero. If such a student_id cannot be found, for example
'260245896', then raise a ValueError with a message 'A student with id 260245896 either
doesn't exist or is not reported as sick.' If the student is a patient zero themselves,
then the minimum distance is 0, otherwise if the student appears in a patient zero’s
contact list, then the minimum distance between the student and a patient zero is 1,
and so on.

>>> contact_tracker.min_distances_from_patient_zeros('260808934')
0

>>> contact_tracker.min_distance_from_patient_zeros('260248711')
1

>>> contact_tracker.min_distance_from_patient_zeros('260561504')
1
"""
        valid_id= False
        student_obj = None
        
        for student in self.students:
            
            if student.student_id == student_id:
                valid_id = True
                student_obj = student
                break
        
        if not valid_id:
            error = " either doesn't exist or is not reported as sick."
            raise ValueError('A student with id '+str(student_id)+ error)
            
        
        minimum_distance= 0
        
        test_list=self.patient_zeros()
        
        if student_obj in test_list:
            
            return minimum_distance
        
#if student is not in patient zeros, check their contacts, and then their contacts and so on
        while student_obj not in test_list:
            new_test_list = []
            
            for student in test_list:
                
                if student.student_id in self.get_all_contacts():
                    student_contacts = self.get_contacts_by_student_id(student.student_id)
                    
                    for contact in student_contacts:
                        new_test_list.append(contact)
            
            test_list=new_test_list
            
            
            minimum_distance+=1
        
        return minimum_distance
                
            
    def all_min_distances_from_patient_zeros(self):
        """()-> dictionary
takes no parameters and returns a dictionary where the keys are all the IDs of all the students
(from students attribute). The value for each student ID is the corresponding student’s minimum
distance from patient zero.

>>> print(contact_tracker.all_min_distances_from_patient_zeros())
{'260808934': 0, '260840155': 1, '260248711': 1, '260996175': 1, '260476020': 1, '260561504': 1,
'260675874': 0, '260758421': 2, '260386543': 0, '260212160': 2, '260970944': 2}

>>> print(contact_tracker.all_min_distances_from_patient_zeros())
{'260111111': 0, '260123456': 1, '260456012': 1, '260996175': 0, '260476020': 0, '260561504': 0}

<<< print(contact_tracker.all_min_distances_from_patient_zeros())
{'260456123': 0, '260999111': 1}
"""
        all_min_distances ={}
        
        for student in self.students:
            min_distance = self.min_distance_from_patient_zeros(student.student_id)
            all_min_distances[student.student_id] = min_distance
            
        return all_min_distances


