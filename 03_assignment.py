'''
Assignment #3 

1. Add / modify code ONLY between the marked areas (i.e. "Place code below"). Do not modify or add code elsewhere.
2. Run the associated test harness for a basic check on completeness. A successful run of the test cases does not guarantee accuracy or fulfillment of the requirements. Please do not submit your work if test cases fail.
3. To run unit tests simply use the below command after filling in all of the code:
    python 03_assignment.py
  
4. Unless explicitly stated, please do not import any additional libraries but feel free to use built-in Python packages
5. Submissions must be a Python file and not a notebook file (i.e *.ipynb)
6. Do not use global variables
7. Make sure your work is committed to your master branch in Github
8. Use the test cases to infer requirements wherever feasible


'''
import csv, json, math, pandas as pd, requests, unittest, uuid

# ------ Create your classes here \/ \/ \/ ------

# Box class declaration below here
class Box():
        """ A class to manufacture box objects"""
        
        def __init__(self, length, width):
            self._length = length
            self._width = width
            
        def __eq__(self, other):
            return self._width == other._width and self._length == other._length 
            
        def get_length(self):
            return self._length
    
        def get_width(self):
            return self._width
        
        def render(self):
           rchar = '*'
           for i in range(0, self._width):
            print (rchar*self._length)
        
        def invert(self):
            self._width,self._length = self._length,self._width
   
        def print_dim(self):
            print ('lenght ' , '%g' % self._length)
            print ('width ' ,  '%g'  % self._width)
    
        def get_dim(self):
            return(self._length, self._width)
    
        def get_area(self):
            a = self._width*self._length
            return a
    
        def get_perimeter(self):
            p = 2*self._width + 2*self._length
            return p
 
        def double(self):
            self._length = 2*(self._length)
            self._width = 2*(self._width)
            return self

        def combine(self,box1):
            self._width = self._width + box1._width
            self._length = self._length + box1._length
            return self      

        def get_hypot(self):  
            return math.sqrt(self._width**2 + self._length**2)
    

    

# MangoDB class declaration below here

class MangoDB():
   """ A collection of dictionaries"""

   def __init__(self): 
       self.rtkey = "default"
       self.ntdkey = "version"
       self.ntdval = "1.0"
       self.ntdict = {self.ntdkey:self.ntdval}
       self.col = {self.rtkey: self.ntdict}
       self.ntdkey = "db"
       self.ntdval = "mangodb"
       self.ntdict.update({self.ntdkey:self.ntdval})
       self.ntdkey = "uuid"
       self.ntdval = str(uuid.uuid4())
       self.ntdict.update({self.ntdkey:self.ntdval})
       
   def add_collection(self, rtname):
       self.rtkey = rtname
       self.col.update({self.rtkey:{}})
       
   def update_collection(self, rtname, addict):
       if rtname not in self.col:
           print("collection not found")
       else:
           ntdict = self.col[rtname]
           ntdict.update(addict)
           self.col.update({self.rtkey:ntdict})
           
   def remove_collection(self, rtname):
       if rtname not in self.col:
           print ("collection not found")
       else:
           del self.col[rtname]
           
   def get_collection_size(self, rtname):
       if rtname not in self.col:
           print ("collection not found")
       else:
          ntdict = self.col[rtname] 
          return len(ntdict)
   
   def get_collection_names(self):
       listcol = []
       for self.rtkey in self.col.keys():
           listcol.append(self.rtkey)
#       print(listcol)    
       return listcol
  
   def list_collection(self):
       listcol = []
       for self.rtkey in self.col.keys():
           listcol.append(self.rtkey)
       return listcol
   
   def to_json(self, rtname):
       jstr = ''
       if rtname not in self.col:
           print ("collection not found")
       else:  
          ntdict = self.col[rtname]  
#          jstr += str(json.dumps(ntdict, indent=4,sort_keys=True))
          jstr += str(json.dumps(ntdict))
#          print(jstr)
       return jstr
          
    
   def display_all_collections(self):
       print(json.dumps(self.col, indent=4,sort_keys=True))
       
   def display_collection_uuid(self):
       self.rtkey = "default"
       self.ntdkey = "uuid"
       return self.col[self.rtkey][self.ntdkey] 

   def wipe(self):
       listcol = []
       for self.rtkey in self.col.keys():
           listcol.append(self.rtkey)
       for key in listcol:
           del self.col[key]
       self.rtkey = "default"
       self.ntdkey = "version"
       self.ntdval = "1.0"
       self.ntdict = {self.ntdkey:self.ntdval}
       self.col = {self.rtkey: self.ntdict}
       self.ntdkey = "db"
       self.ntdval = "mangodb"
       self.ntdict.update({self.ntdkey:self.ntdval})
       self.ntdkey = "uuid"
       self.ntdval = str(uuid.uuid4())
       self.ntdict.update({self.ntdkey:self.ntdval})
            
      

# ------ Create your classes here /\ /\ /\ ------





def exercise01():

    '''
        Create an immutable class Box that has private attributes length and width that takes values for length and width upon construction (instantiation via the constructor). Make sure to use Python 3 semantics. Make sure the length and width attributes are private and accessible only via getters.
        
        Remember, here immutable means there are no setter methods. States can change with the methods required below i.e. combine(), invert().
        
        In addition, create...
        - A method called render() that prints out to the screen a box made with asterisks of length and width dimensions
        - A method called invert() that switches length and width with each other
        - Methods get_area() and get_perimeter() that return appropriate geometric calculations
        - A method called double() that doubles the size of the box. Hint: Pay attention to return value here
        - Implement __eq__ so that two boxes can be compared using ==. Two boxes are equal if their respective lengths and widths are identical.
        - A method print_dim that prints to screen the length and width details of the box
        - A method get_dim that returns a tuple containing the length and width of the box
        - A method combine() that takes another box as an argument and increases the length and width by the dimensions of the box passed in
        - A method get_hypot() that finds the length of the diagonal that cuts throught the middle

        In the function exercise01():
        - Instantiate 3 boxes of dimensions 5,10 , 3,4 and 5,10 and assign to variables box1, box2 and box3 respectively 
        - Print dimension info for each using print_dim()
        - Evaluate if box1 == box2, and also evaluate if box1 == box3, print True or False to the screen accordingly
        - Combine box3 into box1 (i.e. box1.combine())
        - Double the size of box2
        - Combine box2 into box1
        - Using a for loop, iterate through and print the tuple received from calling box2's get_dim()
        - Find the size of the diagonal of box2

'''

    # ------ Place code below here \/ \/ \/ ------
    
       
    box1 = Box(5,10)
    box2 = Box(3,4)
    box3 = Box(5,10)
    box1.print_dim()
    box2.print_dim()
    box3.print_dim()
    print(box1==box2)
    print(box1==box3)
    box1.combine(box3)
    box2.double()
    box1.combine(box2)
    t = box2.get_dim()
    for i in t:
        print (i)
    diag = box2.get_hypot
    print(diag)
      
    
    return box1, box2, box3

    # ------ Place code above here /\ /\ /\ ------


def exercise02():
    '''
    Create a class called MangoDB. The MangoDB class wraps a dictionary of dictionaries. At the the root level, each key/value will be called a collection, similar to the terminology used by MongoDB, an inferior version of MangoDB ;) A collection is a series of 2nd level key/value paries. The root value key is the name of the collection and the value is another dictionary containing arbitrary data for that collection.

    For example:

        {
            'default': {
            'version':1.0,
            'db':'mangodb',
            'uuid':'0fd7575d-d331-41b7-9598-33d6c9a1eae3'
            },
        {
            'temperatures': {
                1: 50,
                2: 100,
                3: 120
            }
        }
    
    The above is a representation of a dictionary of dictionaries. Default and temperatures are collections or root keys. The default collection has a series of key/value pairs that make up the collection. The MangoDB class should create the default collection, as shown, on instantiation including a randomly generated uuid using the uuid4() method and have the following methods:
        - display_all_collections() which iterates through every collection and prints to screen each collection names and the collection's content underneath and may look something like:
            collection: default
                version 1.0
                db mangodb
                uuid 739bd6e8-c458-402d-9f2b-7012594cd741
            collection: temperatures
                1 50
                2 100 
        - add_collection(collection_name) allows the caller to add a new collection by providing a name. The collection will be empty but will have a name.
        - update_collection(collection_name,updates) allows the caller to insert new items into a collection i.e. 
                db = MangoDB()
                db.add_collection('temperatures')
                db.update_collection('temperatures',{1:50,2:100})
        - remove_collection() allows caller to delete the collection and its associated data
        - list_collections() displays a list of all the collections
        - get_collection_size(collection_name) finds the number of key/value pairs in a given collection
        - to_json(collection_name) that converts the collection to a JSON string
        - wipe that cleans out the db and resets it with just a default collection
        - get_collection_names() that returns a list of collection names

        Make sure to never expose the underlying data structures

        For exercise02(), perform the following:

        - Create an instance of MangoDB
        - Add a collection called testscores
        - Take the test_scores list and insert it into the testscores collection, providing a sequential key i.e 1,2,3...
        - Display the size of the testscores collection
        - Display a list of collections
        - Display the db's UUID
        - Wipe the database clean
        - Display the db's UUID again, confirming it has changed
    '''

    test_scores = [99,89,88,75,66,92,75,94,88,87,88,68,52]

    # ------ Place code below here \/ \/ \/ ------
    db = MangoDB()
    db.add_collection('test_scores')
    test_scores = {1:99,2:89,3:88,4:75,5:66,6:92,7:75,8:94,9:88,10:87,11:88,12:68,13:52}
    db.update_collection('test_scores', test_scores)
    print(db.col)
    size=db.get_collection_size('test_scores')
    print(size)
    listcol=db.list_collection()
    print(listcol)
    jform = db.to_json('test_scores')
    print(jform)
    print(db.display_collection_uuid())
    db = MangoDB()
    print(db.display_collection_uuid())
        

    # ------ Place code above here /\ /\ /\ ------


def exercise03():
    """
    1. Avocado toast is expensive but enormously yummy. What's going on with avocado prices? Read about avocado prices on Kaggle (https://www.kaggle.com/neuromusic/avocado-prices/home)
    2. Load the included avocado.csv file and display every line to the screen
    3. Use the imported csv library
    """   
    

    # ------ Place code below here \/ \/ \/ ------
    
    with open("avocado.csv") as f:
        reader = csv.reader(f)
        data = [r for r in reader]
 #       data.pop(0)
    
    for ln in data:     
       print(ln)
       
    # ------ Place code above here /\ /\ /\ ------

class TestAssignment3(unittest.TestCase):
    def test_exercise01(self):
        print('Testing exercise 1')
        b1, b2, b3 = exercise01()
        self.assertEqual(b1.get_length(),16)
        self.assertEqual(b1.get_width(),28)
        self.assertTrue(b1==Box(16,28))
        self.assertEqual(b2.get_length(),6)
        self.assertEqual(b2.get_width(),8)
        self.assertEqual(b3.get_length(),5)
        self.assertEqual(b2.get_hypot(),10)
        self.assertEqual(b1.double().get_length(),32)
        self.assertEqual(b1.double().get_width(),112)
        self.assertTrue(6 in b2.get_dim())
        self.assertTrue(8 in b2.get_dim())
        self.assertTrue(b2.combine(Box(1,1))==Box(7,9))

    def test_exercise02(self):
        print('Testing exercise 2')
        db = MangoDB()
        self.assertEqual(db.get_collection_size('default'),3)
        self.assertEqual(len(db.get_collection_names()),1)
        self.assertTrue('default' in db.get_collection_names() )
        db.add_collection('temperatures')
        self.assertTrue('temperatures' in db.get_collection_names() )
        self.assertEqual(len(db.get_collection_names()),2)
        db.update_collection('temperatures',{1:50})
        db.update_collection('temperatures',{2:100})
        self.assertEqual(db.get_collection_size('temperatures'),2)
        self.assertTrue(type(db.to_json('temperatures')) is str)
        self.assertEqual(db.to_json('temperatures'),'{"1": 50, "2": 100}')
        db.wipe()
        self.assertEqual(db.get_collection_size('default'),3)
        self.assertEqual(len(db.get_collection_names()),1)
        
    def test_exercise03(self):
        print('Exercise 3 not tested')
        exercise03()
     

if __name__ == '__main__':
    unittest.main()
