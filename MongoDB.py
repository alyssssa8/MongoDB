from faker import Factory
from math import floor
from random import randint
from datetime import date
from datetime import timedelta 

import json
import random
import time
from array import *
# functions to generate random values
from random import expovariate, normalvariate, choice, randint, random, shuffle



CURRENT_CARD_ID = 0
CARD_START= date(2018,5,15)
CARD_END = date(2018,8,20)
SENIOR_MANAGER_SIZE = 200
MANAGER_SIZE = 3000
EMPLOYEE_SIZE = 30000
TOTAL_EMPLOYEE_SIZE = SENIOR_MANAGER_SIZE+MANAGER_SIZE+EMPLOYEE_SIZE
CARD_FINISH_DAY = 10
NUMBER_MEMBER = 4
COMMENT_SIZE = 20
EMPLOYEE_START_AGE = 18
EMPLOYEE_RETAIED_AGE = 55
START_CARD_DATE = date(2018, 1, 1)
END_CARD_DATE = date(2018, 5, 15)

GENERATE = 10000

CONTENT = ('Poor', 'Needs Improvement', 'There is a bug for the project, can anyone can fix that.', 'I will fix it soon',
            'Sounds good!', 'I still can go', 'Our meeting was changed', 'Meets Requirements',
            'I assigned a new project.', 'Got it', 'Ok', 'This project is so hard. ',
            'Good', 'For porject, there are logical problem, can anyone take a look', 'I could not join the meetting becasue of time conflic', 'Fairly authentic',
            'Exceeds Requirements', 'Outstanding', 'will go to lunch', 'will be back soon')
       
POSITION= ('Senior Manager', 'Manager', 'Employee')
ACCESS = ('admin', 'user')
TYPE = ('card', 'user')

# Faker random value generator
generator = Factory.create()

# Output files
store_file = None
class card(object):
    def __init__(self, type,card_id, owner_id,create_date,due_date,member,comment):
        self.type = type       
        self.create_date = create_date
        self.due_date = due_date
        self.card_id = card_id
        self.owner_id = owner_id
        self.member = member
        self.comment = comment
    def __str__(self):
        '''
        Return JSON string for entire card document,
        compatible with mongoimport
        '''
        carddict = {}
        carddict["type"] = self.type
        carddict["create_date"] = str(self.create_date)
        carddict["due_date"] = str(self.due_date)
        carddict["card_id"] = self.card_id
        carddict["owner_id"] = self.owner_id
        carddict["member"] = self.member
        carddict["comment"] = self.comment
        return json.dumps(carddict)  #JSON is an way to represent your class instance in a string

class user(object):
    def __init__(self, type, access, position, user_id, age, supervisor_id, username):
        self.type = type
        self.access = access
        self.position = position
        self.user_id = user_id
        self.age = age
        self.supervisor_id = supervisor_id
        self.username = username
      
    def __str__(self):
        '''
        Return JSON string for entire user document,
        compatible with mongoimport
        '''
        carddict = {}
        carddict["type"] = self.type
        carddict["access"] = self.access
        carddict["position"] = self.position
        carddict["user_id"] = self.user_id
        carddict["age"] = self.age
        carddict["supervisor_id"] = self.supervisor_id
        carddict["username"] = self.username
        return json.dumps(carddict)

def gen_from_prob_table(probabilities):
    '''
    Return a random integer from 1 to len(probabilities),
    following the cumulative probabilities of the parameter
    '''
    rand_val = random()
    prob_index = 0
    while prob_index < len(probabilities):
        if rand_val < probabilities[prob_index]:
            break
        prob_index += 1
    return prob_index + 1

def gen_comment(project_index):
    '''
    generate comment
    '''
    comment = []
    my_comment_size = randint(0, COMMENT_SIZE)
    for project_index2 in range(my_comment_size):
        comment.append(gen_each_content(project_index))    
    return comment

def gen_each_content(project_index):    
    content=choice(CONTENT)
    return {"author_id:": randint(0,TOTAL_EMPLOYEE_SIZE),"belong_to_card_id:":project_index, "content": content}

def gen_member():
    '''
    generate member
    '''
    member = []
    number_of_member=randint(0, NUMBER_MEMBER)
    for each_member in range(number_of_member):
        member.append( randint(0,TOTAL_EMPLOYEE_SIZE))
    return member

def gen_card_id(project_index):
    '''
    generate card_id
    '''
    card_id = project_index   
    return card_id

def gen_owner_id():
    '''
    generate owner_id     
    '''
    owner_id = randint(0, SENIOR_MANAGER_SIZE + MANAGER_SIZE-1)
    return owner_id

def gen_create_date():
    '''
    http://faker.readthedocs.io/en/master/providers/faker.providers.date_time.html
    generate create date
    '''
    create_date = generator.date_time_between_dates(START_CARD_DATE, END_CARD_DATE)
    return create_date

def gen_due_date(create_date):
    '''
    generate card due date
    '''
    due_date = create_date + timedelta(days=CARD_FINISH_DAY)
    return due_date

def gen_access(project_index):
    ''' 
    Generate access
    ''' 
    if project_index < SENIOR_MANAGER_SIZE+ MANAGER_SIZE:
       result = "admin"
    else:
        result = "user"
    return result

def gen_position(project_index):
    ''' 
    Generate position
    ''' 
    if project_index < SENIOR_MANAGER_SIZE:
       result = "Senior Manager"
    else:
        if project_index < MANAGER_SIZE:
            result = "Manager"    
        else:
            result = "employee"
    return result


def gen_user_id(project_index):
    ''' 
    Generate user_id
    ''' 
    user_id = project_index    
    return user_id

def gen_age():
    '''
   Generate age
    ''' 
    return randint(EMPLOYEE_START_AGE, EMPLOYEE_RETAIED_AGE)

def gen_supervisor_id(project_index):
    ''' 
    Generate supervisor_id
    ''' 
    if project_index < SENIOR_MANAGER_SIZE:
       result = -1
    else:
        if project_index < MANAGER_SIZE:
            result = randint(0,SENIOR_MANAGER_SIZE)   
        else:
            result = randint(SENIOR_MANAGER_SIZE,MANAGER_SIZE-1)
    return result

def gen_username():
    ''' 
    Generate username
    ''' 
    first_name = generator.first_name()
    last_name = generator.last_name()
    return{"firstName":first_name, "lastName":last_name}

def generate_single_card(project_index):
    ''' 
    Generate fields for one card
    '''    
    create_date = gen_create_date()
    new_card = card("card",
                    gen_card_id(project_index),
                    gen_owner_id(), create_date,
                    gen_due_date(create_date),
                    gen_member(),
                    gen_comment(project_index))
  
    store_file.write(str(new_card) + '\n') 
    return new_card
def generate_single_user(project_index):
    ''' 
    Generate fields for one user
    '''    
    new_user = user("user",
                    gen_access(project_index),
                    gen_position(project_index),
                    gen_user_id(project_index),
                    gen_age(),
                    gen_supervisor_id(project_index),
                    gen_username())
        
    store_file.write(str(new_user) + '\n')
    return new_user
def generate_project(num_projects):
    '''
    Generate card and user
    '''
    for project_index in range(num_projects):
        generate_single_card(project_index)

    for project_index in range(TOTAL_EMPLOYEE_SIZE):
        generate_single_user(project_index)
    store_file.close()
        
if __name__ == '__main__':
    import sys
    store_file = open('.\\stores_temp.json', 'w')

    if len(sys.argv) == 1:
        to_generate = 1000
    else:
        to_generate = int(sys.argv[1])
    generate_project(GENERATE)

            

