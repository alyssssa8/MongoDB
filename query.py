from HW4TurnIn import *
from random import choice, random, randint

# to get first "page" of results
FIND_LIMIT = 20
COMMENT_PROB = 0.5
AGE_PROB = 0.5

def gen_key_query(key, value):
    '''
    Generate query with value for one field of card or user
    '''

    if ( "id" in key ):
        value = value.replace('"', '')
    query_file.write('result = db.card.find({'
                     + key + ':'
                     + value
                     +'}, {owner_id:1,card_id:1,user_id:1,_id:0}).limit('
                     + str(FIND_LIMIT) + ');\n')
    query_file.write("print('find:"
                      + key + " match it is value.');\n")
    #Generate code to output result
    query_file.write('''while ( result.hasNext() ) {
    printjson( result.next() );
}
''')
       
def gen_key_query_2(key1, value1, key2, value2):
    '''
    Generate query with value for one field of card or user
    '''

    query_file.write('result = db.card.find({'
                     + key1 + ':'
                     + value1 + ', '
                     + key2 + ':'
                     + value2
                     +'}, {owner_id:1,card_id:1,user_id:1,_id:0}).limit('
                     + str(FIND_LIMIT) + ');\n')
    query_file.write("print('find:"
                      + key1 + " " + key2 + " match it is value.');\n")
    #Generate code to output result
    query_file.write('''while ( result.hasNext() ) {
    printjson( result.next() );
}
''')

def gen_post_comment_query(match, review):
    '''
    Generate "post _comment_query" query
    '''
    query_file.write('result = db.card.update(' + match +
                        ', {$push:{"comment":' + review +
                       '}});\n')
                
    query_file.write('''
    print("update: :");
    printjson( result);
''')


def gen_avg_age_query(key, value):
    '''
    Generate query to get average age of each position
    '''
    query_file.write('''
result = db.card.aggregate(
   [
     { $match : { "position": { $ne: null } }}, 
     {
       $group:
         {
           _id: "$position",
           avg_age: { $avg: "$age" }
         }
     }
   ]
)

print("aggregate: The age of user with an average age");

while ( result.hasNext() ) {

   printjson( result.next() );

}
''')

def gen_insert_query(count):
    user_index = TOTAL_EMPLOYEE_SIZE + count
    user_name = gen_username()
    query_file.write('result = db.card.insert( { ' + 
                     'type: "user", ' +
                     'user_id: ' + str(user_index) + ", " +
                     'access: ' + surround(gen_access(user_index), '"') + ", " +
                     'position: ' + surround(gen_position(user_index), '"') + ", " +
                     'age: ' + str(gen_age()) + ", " + 
                     'supervisor_id: ' + str(gen_supervisor_id(user_index)) + ", " +
                     'username: { ' + 
                     'firstName: ' + surround(user_name['firstName'], '"') + ", " +
                     'lastName: ' + surround(user_name['lastName'], '"') + "} } )\n")
    query_file.write("printjson( result )\n");



# Wrap some text with the chosen character on both ends
# (of course, could be any string)
def surround(text, quotes):
    return quotes + text + quotes

# JavaScript constants for boolean values
JS_BOOLS = ('true', 'false')

def gen_type_params():
    '''
       generate type field and random value
    '''
    return ['type', surround(choice(TYPE), '"')]

def gen_due_date_params():
    '''
       generate due_date field and random value    
    '''  
    return ['due_date', surround(str(gen_due_date(gen_create_date())),'"')]

#generate create date field and random value 
def gen_create_date_params():
   
    return ['create_date', surround(str(gen_create_date()),'"')]

#generate owner_id field and random value
def gen_owner_id_params():
   
    return ['owner_id', surround(str(gen_owner_id()), '"')]

#generate card_id field and random value
def gen_card_id_params():
   
    return ['card_id',surround(str(gen_card_id(GENERATE)), '"') ]

# generate access field and random value
def gen_access_params():

    return['access', surround(choice(ACCESS),'"')]

# generate positon field and random value
def gen_position_params():
    
    return ['position', surround(choice(POSITION),'"')]
#generate user_id field and random value
def gen_user_id_params():
   
    return ['user_id', surround(str(gen_user_id()), '"')]

# generate age field and random value
def gen_age_params():
  
    return ['age', surround(str(gen_age()), '"')]

#generate supervisor_id field and random value
def gen_supervisor_id_params():
  
    return ['supervisor_id', surround(str(gen_supervisor_id()), '"')]

#Generate commands to initialize connection to database
def gen_connection():
   
    query_file.write('''
// A script to read from a collection of stores in the local database
conn = new Mongo();

// connect to the local database
db = conn.getDB("project");
'''
)

ids = []
# get id  
# Get valid _id values from file, which is generated by get_ids.js
               
def read_ids():
   
    ids_file = open('.\\id.txt', 'r')
    for id_doc in ids_file:
        ids.append(id_doc.replace('\n',''))
    ids_file.close()

# generate id 
# Return random id for document
                    
def gen_id_doc():
  
    return choice(ids)

# functions that generate different types of queries
QUERY_GENERATORS = (gen_key_query,gen_avg_age_query)

# functions that generate queries on different fields
PARAM_GENERATORS = (gen_type_params,gen_due_date_params,gen_create_date_params,
                    gen_owner_id_params,gen_card_id_params,gen_access_params, gen_position_params, gen_user_id_params, gen_age_params, gen_supervisor_id_params )                          
                          
# Generate the queries              
def generate_queries(to_generate):
    query_ct = 0
    while query_ct < to_generate:
        query_ct += 5

        QUERY_GENERATORS[gen_from_prob_table((AGE_PROB,1.0))-1](*PARAM_GENERATORS[gen_from_prob_table((.1,.2,.3,.5,.6,7,.9,.8,.95,1.0))-1]())
        gen_avg_age_query(None, None)
        gen_key_query(*PARAM_GENERATORS[gen_from_prob_table((.1,.2,.3,.5,.6,7,.9,.8,.95,1.0))-1]())
        #gen_key_query_2("supervisor_id", str(randint(0, SENIOR_MANAGER_SIZE+MANAGER_SIZE)), "age", str(randint(EMPLOYEE_START_AGE, EMPLOYEE_RETAIED_AGE)))
        gen_post_comment_query(gen_id_doc(),str(gen_each_content(randint(0, GENERATE))))
        gen_insert_query(query_ct)
        
# To run:
# python generate_queries.py [num_queries [output_file
# 	[probability of no queries for average age
#         [probability of having reviews for a store]]]]
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        to_generate = 1000
    else:
        to_generate = int(sys.argv[1])
    fname = '.\\query.js'
    if len(sys.argv) > 2:
        fname = sys.argv[2]
        if len(sys.argv) > 3:
            AGE_PROB = float(sys.argv[3])
            if len(sys.argv) > 4:
                COMMENT_PROB = float(sys.argv[4])
                
    query_file = open(fname,'w')
    read_ids()
    gen_connection()
    generate_queries(to_generate)
    query_file.close()
