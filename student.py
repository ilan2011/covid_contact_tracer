
class Student:
    """
class representing a student
"""

    
    def __init__(self, student_id, name, is_sick = False):
        """(str,str,bool)-> Student
the constructor for the class, takes three inputs to initiate the attributes of the class
– the student id (string), the student name (string) and a boolean variable indicating whether
the student is sick. The latter has a default value False. Raises Value error if student id
is not a valid ID.

>>> larry = Student('260745567', 'Larry', True)
>>> type(larry)
<class 'student.Student'>

>>> sherry = Student('260745567', 'Sherry')
>>> type(sherry)
<class 'student.Student'>

>>> sherry = Student('abcdef', 'Sherry')
Traceback (most recent call last):
ValueError: The student ID abcdef is not a valid ID
"""
        is_valid = self.is_valid_id(student_id)
        
        if not is_valid:
            raise ValueError("The student ID "+student_id+" is not a valid ID")
        
        self.student_id = student_id
        self.name = name
        self.is_sick = is_sick
       
        
    def __str__(self):
        """(self)-> string
returns string for student object in format: Name (student_id)

>>> larry = Student('260745567', 'Larry', True)
>>> str(larry)
'Larry (260745567)'

>>> josh = Student('260743566', 'Josh')
>>> str(josh)
'Josh (260743566)'

>>> tam = Student('260741111', 'Tam')
>>> str(tam)
'Tam (260741111)'
"""
        name = self.name
        student_id = self.student_id
        
        return name+" ("+student_id+")"
        
    def __repr__(self):
        """(self)-> string
returns same string as __str___.
overwrites the printable representation of the object

>>> larry = Student('260745567', 'Larry', True)
>>> repr(larry)
'Larry (260745567)'
>>> larry
Larry (260745567)

>>> josh = Student('260743566', 'Josh')
>>> str(josh)
'Josh (260743566)'
>>> josh
'Josh (260743566)'

>>> tam = Student('260741111', 'Tam')
>>> str(tam)
'Tam (260741111)'
>>> tam
'Tam (260741111)'
"""
        return str(self)
    
    @staticmethod
    def is_valid_id(student_id):
        """(str)-> boolean
takes an input string for a student id and checks whether it is a valid McGill ID.
An ID string is valid if it is a has 9 digits where the first three digits are 260.

>>> Student.is_valid_id('260745567')
True

>>> Student.is_valid_id('260741234')
True

>>> Student.is_valid_id('abc')
False
"""
        digits = "0123456789"
        
        for char in student_id:
            
            if char not in digits:
                return False
        
        return len(student_id) == 9 and student_id[0:3] == "260"
    
    @classmethod
    def from_JSON(cls, json_data):
        """(str)-> Student
constructs and return a Student object from the input parameter
string that has the data of the student in JSON.

>>> larry = Student.from_JSON('{"id": "260745567", "name": "Larry"}')
>>> str(larry)
'Larry (260745567)'

>>> jay = Student.from_JSON('{"id": "260744443", "name": "Jay"}')
>>> str(jay)
'Jay (260744443)'

>>> jay = Student.from_JSON('{"id": "260744443", "name": "Jay"}')
>>> str(jay)
'Jay (260744443)'

>>> peter = Student.from_JSON('{"id": "260123456", "name": "Peter"}')
>>> str(peter)
'Peter (260123456)'
"""
        id_str = ""
        name_str = ""
        keys_and_vals = json_data.split(",")
        
        for index, pair in enumerate(keys_and_vals):
            
            if index == 0: 
                id_str = pair[8:-1] #id index is constant
            
            else:
                name_str = pair[10:-2] # name index is constant
        
        return cls(id_str,name_str)
        
