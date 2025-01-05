import json 
import copy
import time
import sys
from copy       import deepcopy
from typing     import List,Union

class GaitIdxSeqsType:
    __slots__ = ("gait_seqs","name","map_nam2indx","sqs_len")
    def __init__(self, gait_seqs=None, name=None):

        # Row: pose sequence number. Colum: leg number.  
        seqs_tmplt = \
        {
        0  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t0  step1.1 move lfnt leg" },
        1  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":1,"mode":"pose","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t1  step1.2 move lfnt leg" },
        2  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":2,"mode":"pose","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t2  step1.3 move lfnt leg" },
        3  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"torq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t3  step1.4 move lfnt leg" },
        4  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t4  step2.1 move rfnt leg" },
        5  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":1,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t5  step2.2 move rfnt leg" },
        6  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":2,"mode":"pose","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t6  step2.3 move rfnt leg" },
        7  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"torq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t7  step2.4 move rfnt leg" },
        8  : {"rm": {"idx":0,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t8  step3.1 move midd leg" },
        9  : {"rm": {"idx":1,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":1,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t9  step3.2 move midd leg" },
        10 : {"rm": {"idx":2,"mode":"pose" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":2,"mode":"pose","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t10 step3.3 move midd leg" },
        11 : {"rm": {"idx":3,"mode":"torq" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":3,"mode":"torq","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t11 step3.4 move midd leg" },
        12 : {"rm": {"idx":3,"mode":"porq" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lb": {"idx":0,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":0,"mode":"pose","force_dir":[1,0,1]} ,"name": "t12  step4.1 move bak leg" },
        13 : {"rm": {"idx":3,"mode":"porq" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lb": {"idx":1,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":1,"mode":"pose","force_dir":[1,0,1]} ,"name": "t13  step4.2 move bak leg" },
        14 : {"rm": {"idx":3,"mode":"porq" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lb": {"idx":2,"mode":"pose","force_dir":[1,0,1]},"rb": {"idx":2,"mode":"pose","force_dir":[1,0,1]} ,"name": "t14  step4.3 move bak leg" },
        15 : {"rm": {"idx":3,"mode":"porq" ,"force_dir":[1,0,1]},"rf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lf": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lm": {"idx":3,"mode":"porq","force_dir":[1,0,1]},"lb": {"idx":3,"mode":"torq","force_dir":[1,0,1]},"rb": {"idx":3,"mode":"torq","force_dir":[1,0,1]} ,"name": "t15  step4.4 move bak leg" }
        }
        # Leg index order is: 0:rm, 1:rf,...counter-clock... 5:rb
        self.map_nam2indx = ["rm","rf","lf","lm","lb","rb"]

        if (gait_seqs == None):
            self.gait_seqs = seqs_tmplt
        else: 
            self.gait_seqs = deepcopy(gait_seqs)
             
        self.name  = name

    def key_str2int(self,str_key_dic):
        '''
        After json.load(out_file), json does not support int type key in dictionary, 
        so I created this function to do that.

        :param str_key_dic : A dictionary which its' key is a str(int) type
        :type  str_key_dic : Dictionary 
        
        :return int_key_dic: A dictionary which its' key is a int type 
        :type   int_key_dic: Dictionary 
        '''
    
        int_key_dic = dict()
        for strkey in str_key_dic:
            int_key_dic[int(strkey)] = str_key_dic[strkey]
        
        return int_key_dic
   

    def get_sqs_len(self):
        return len(self.gait_seqs)
    
    def get_by_nam(self,tim_idx,leg_nam_str):
        return self.gait_seqs[tim_idx][leg_nam_str]["idx"]
    
    def get_by_idx(self,tim_idx,leg_idx):
        # tim_idx: time step index
        # leg_idx: leg index, range[0,5] 
        leg_nam_str = self.map_nam2indx[leg_idx]
        return self.gait_seqs[tim_idx][leg_nam_str]["idx"]

    def set_mode_by_idx(self,tim_idx,leg_idx,mode_str):
        # tim_idx: time step index
        # leg_idx: leg index, range[0,5] 
        # mode_str: A string, which is the mode of the leg, pose or torq or porq
        leg_nam_str = self.map_nam2indx[leg_idx]
        self.gait_seqs[tim_idx][leg_nam_str]["mode"] = mode_str
        
    def get_mode_by_idx(self,tim_idx,leg_idx):
        # tim_idx: time step index
        # leg_idx: leg index, range[0,5] 
        # return: A string, which is the mode of the leg, pose or torq or porq
        leg_nam_str = self.map_nam2indx[leg_idx]
        return self.gait_seqs[tim_idx][leg_nam_str]["mode"] 
    
    def get_force_by_idx(self,tim_idx,leg_idx)->list[Union[int,int,int]]:

        # tim_idx: time step index
        # leg_idx: leg index, range[0,5] 
        # return: A 3 element list, which is the force direction
        
        leg_nam_str = self.map_nam2indx[leg_idx]
        return self.gait_seqs[tim_idx][leg_nam_str]["force_dir"]

    def get_seqs_by_idxs(self,star_tim_idx,end_tim_idx,star_leg_idx,end_leg_idx):
        # return: A 2*2 matrix Row: time unit. Colum: legs index
        seq_mat = []

        if(end_tim_idx>star_tim_idx and end_leg_idx>star_leg_idx):
            for t_idx in range(star_tim_idx,end_tim_idx): # loop each row 
                one_leg_seqs =[]
                for leg_idx in range(star_leg_idx,end_leg_idx):
                    one_leg_seqs = one_leg_seqs+[self.get_by_idx(t_idx,leg_idx)]
                seq_mat = seq_mat+[one_leg_seqs]
        return seq_mat
    
    def get_dict(self):
        return self.gait_seqs
    
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key

        '''
        self.gait_seqs = self.key_str2int(json_str)

 
    def __str__(self):
        #self.gait_seqs
        rstr=''
        for key in self.gait_seqs:
            rstr = rstr+ str(key) + ": "+str(self.gait_seqs[key]) + "\n"
        return rstr
    
def test_load_json():
    gs1 = GaitIdxSeqsType()
    out_file = open("../config/ctraj_sqs_tright.json", "r") 
    trght_gaits = json.load(out_file)
    gseqs = trght_gaits["GAIT_TRAJ_IDX_SEQS"]

    gs1.set_by_strkey(gseqs)

    gsqs = gs1.get_seqs_by_idxs(0,5,0,6)
    print(gsqs)

def test_load_json2():
    gs1 = GaitIdxSeqsType()

    print("gs1 \n",gs1)
    print(gs1.get_force_by_idx(0,0));    

if __name__ == "__main__":
    #test_load_json()
    test_load_json2()