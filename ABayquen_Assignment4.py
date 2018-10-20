# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 09:22:27 2018

@author: ajb2
"""

import datetime as dt
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unittest
import uuid

class PandasChain:
    # 5 pts - Complete this constructor
    def __init__(self, name): 
        self.__name = name.upper()
        self.__chain = []
        self.__id = hashlib.sha256(str(str(uuid.uuid4())+self.__name+str(dt.datetime.now())).encode('utf-8')).hexdigest()
        self.__seq_id = 0  # Create a sequence ID and set to zero
        self.__prev_hash = str(None) # Set to None
        self.__current_block = Block(self.__seq_id, self.__prev_hash) # Create a new Block 
        print(self.__name,'PandasChain created with ID',self.__id,'chain started.')
        
    # 5 pts - This method should loop through all committed and uncommitted blocks and display all transactions in them
    def display_chain(self): 
        if len(self.__chain) > 0:
            print('Transactions From Committed Block(s):')
            for i in range(len(self.__chain)):
                self.__chain[i].display_transactions()
        if self.__current_block.get_size() > 0: 
            print('Transactions From Uncommitted Block')
            self.__current_block.display_transactions()
        return
        
    # This method accepts a new transaction and adds it to current block if block is not full. 
    # If block is full, it will delegate the committing and creation of a new current block 
    def add_transaction(self,s,r,v): 
        if self.__current_block.get_size() >= 10:
            self.__commit_block(self.__current_block)
        self.__current_block.add_transaction(s,r,v)
        return
        
    # 10 pts - This method is called by add_transaction if a block is full (i.e 10 or more transactions). 
    # It is private and therefore not public accessible. It will change the block status to committed, obtain the merkle
    # root hash, generate and set the block's hash, set the prev_hash to the previous block's hash, append this block 
    # to the chain list, increment the seq_id and create a new block as the current block
    def __commit_block(self,block): 
        self.__current_block.set_status('COMMITTED')
    #   self.__current_block.get_simple_merkle_root()
        hash = str(self.__prev_hash) + str(self.__id) + str(dt.datetime.now()) + str(self.__seq_id) + str(self.__current_block.get_simple_merkle_root())
        phash = self.__current_block.set_block_hash(hash) 
        self.__chain.append(self.__current_block)
        self.__seq_id += 1
        self.__prev_hash = phash 
        self.__current_block = Block(self.__seq_id, self.__prev_hash)
        print('Block committed')
    
    # 10 pts - Display just the metadata of all blocks (committed or uncommitted), one block per line.  
    # You'll display the sequence Id, status, block hash, previous block's hash, merkle hash and total number (count) 
    # of transactions in the block
    def display_block_headers(self):
        if len(self.__chain) > 0:
           for i in range(len(self.__chain)):
               self.__chain[i].display_header()
        if self.__current_block.get_size() > 0: 
            self.__current_block.display_header()
        return
    
    # 5 pts - return int total number of blocks in this chain (committed and uncommitted blocks combined)
    def get_number_of_blocks(self): 
        return self.__seq_id + 1
    
    # 10 pts - Returns all of the values (Pandas coins transferred) of all transactions from every block as a single list
    def get_values(self):
        blval = []
        if len(self.__chain) > 0:
           for i in range(len(self.__chain)):
               blval.extend(self.__chain[i].get_values())
        if self.__current_block.get_size() > 0: 
           blval.extend(self.__current_block.get_values())
        #print(blval)
       # blval = [[50], [51], [52], [53], [53], [53]] 
        return blval
                    
class Block:
 # 5 pts for constructor
    def __init__(self,seq_id,prev_hash): 
        self.__seq_id = seq_id  # Set to what's passed in from constructor
        self.__prev_hash = prev_hash  # From constructor
        self.__col_names = ['Timestamp','Sender','Receiver','Value','TxHash']
        self.__transactions = pd.DataFrame(columns=[self.__col_names])  # Create a new blank DataFrame with set headers
        self.__status = 'UNCOMMITTED' # Initial status. This will be a string.
        self.__block_hash = str(None)
        self.__merkle_tx_hash = str(None)
                
 #5 pts -  Display on a single line the metadata of this block. You'll display the sequence Id, status, 
 # block hash, previous block's hash, merkle hash and number of transactions in the block
    def display_header(self): 
        print('Sequence ID = ', self.__seq_id, ' : ',   \
              'Status = ' , self.__status, ' : ',   \
              'Block Hash = ', self.__block_hash, ' : ',   \
              'Previous Hash = ', self.__prev_hash, ' : ',   \
              'Merkle Transaction Hash = ', self.__merkle_tx_hash, ' : ',   \
              'Number of transactions in the block = ', self.get_size() )
        
        
# 10 pts - This is the interface for how transactions are added
    def add_transaction(self,s,r,v): 
        ts = dt.datetime.now() # Get current timestamp 
        tx_hash = hashlib.sha256(str(str(str(ts)+ s + r + str(v))).encode('utf-8')).hexdigest()
        new_transaction = pd.DataFrame(data=np.array([[ts, s, r, v, tx_hash]]),index=[len(self.__transactions.index)],columns=[self.__col_names])
        frames = [self.__transactions, new_transaction]
        self.__transactions = pd.concat(frames)
        return
        #print(frames)
        
        
### 10 pts -Print all transactions contained by this block
    def display_transactions(self): 
        for index, row in self.__transactions.iterrows():
            print(row[0:])
#        for key, value in self.__transactions.iteritems():
#            print(key, value)
#        for column in self.__transactions:
#            print(self.transactions[column])
#       print(self.__transactions[0]) 
###       f_trans = pd.DataFrame(self.__transactions)
###      print(f_trans)
       
# 5 pts - Setter for status - Allow for the change of status (only two statuses exist - COMMITTED or UNCOMMITTED). 
# There is no need to validate status.
    def set_status(self,status):
        self.__status = status
        return
    
# 5 pts - Setter for block hash
    def set_block_hash(self,hash):
        self.__block_hash = hashlib.sha256(str(hash).encode('utf-8')).hexdigest()
        return self.__block_hash

# 10 pts - Return and calculate merkle hash by taking all transaction hashes, concatenate them into one string and
# hash that string producing a "merkle root" - Note, this is not how merkle tries work but is instructive 
# and indicative in terms of the intent and purpose of merkle tries
    def get_simple_merkle_root(self):  
        for index, row in self.__transactions.iterrows() :
            print(row['TxHash'])
            self.__merkle_tx_hash = self.__merkle_tx_hash + str(row['TxHash'])
        self.__merkle_tx_hash =  hashlib.sha256(str(self.__merkle_tx_hash).encode('utf-8')).hexdigest()   
        
# 5 pts- Return the number of transactions contained by this block
    def get_size(self): 
        return len(self.__transactions.index)
    
    def get_values(self):
        #lval = []
        #val_list = self.__transactions["Value"].values.tolist()
        #print(val_list)
        #for index, row in self.__transactions.iterrows() :
        #    print(row[['Value']])
        #    lval = lval + row['Value']
        #return self.__transactions["Value"].values.tolist() 
        return self.__transactions.loc[:,"Value"].values.tolist()    
        
    
class TestAssignment4(unittest.TestCase):
    def test_chain(self):
        block = Block(1,"test")
        self.assertEqual(block.get_size(),0)
        block.add_transaction("Bob","Alice",49)
        self.assertEqual(block.get_size(),1)
        pandas_chain = PandasChain('testnet')
        self.assertEqual(pandas_chain.get_number_of_blocks(),1)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.get_values()
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),2)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),3)
        plt.plot(list(np.arange(1,1+len(pandas_chain.get_values()))),pandas_chain.get_values())
        plt.show()
             
        
if __name__ == '__main__':
    unittest.main()
