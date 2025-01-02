from copy import deepcopy
import sys 
sys.path.append("../")
from    typing                     import List,Union
from    custom_type.bot_base_type  import BotBaseType
from    utils.print_flush          import print_flush as print

class BotJointType(BotBaseType):

    __slots__ = ("jt_dic","name"   ,"jt_nam_arr",
                 "leg_sz","jont_sz","action_perid")

    def __init__(self, name="",joint_dic=None ):
        if joint_dic is not None: 
            if (isinstance(joint_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')
        # mode: pose, torq, porq

        jtdic_tmplt = \
                {
                0: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-middle", "id": 0},
                1: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-front" , "id": 1},
                2: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-front"  , "id": 2},
                3: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-middle" , "id": 3},
                4: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-back"   , "id": 4},
                5: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-back"  , "id": 5}
                } 
        
        self.leg_sz     = super().LEG_SZ
        self.jont_sz    = super().JOINT_SZ
        self.jt_nam_arr = super().NAMES_JOINT
        self.action_perid = 0

        if joint_dic == None:
            self.jt_dic = jtdic_tmplt
        else: 
            
            if(isinstance(list(joint_dic.keys())[0],str)):
                self.set_by_strkey(joint_dic)
            else:
                self.jt_dic = deepcopy(joint_dic)
        self.name = name

    def check_any_None(self):
        for i in range(self.leg_sz):
            c,f,t = self[i]
            if c==None or f==None or t==None:
                return True
        return False

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

    def form_str(self):
        # Format row coord value
        len_legs = len(self.jt_dic)
        sr_val_ar = [""]*len_legs

        # Loop over each row
        for j in range(len_legs):
            c_str = "coxa: ["
            f_str = " femur: ["
            t_str = " tibia: ["
            
            print("jt_dic: ",j,",",self.jt_dic[j])
            
            c = self.jt_dic[j]["coxa"]["val"]
            f = self.jt_dic[j]["femur"]["val"]
            t = self.jt_dic[j]["tibia"]["val"]

            c_str = c_str + f"{c:+8.2f},"
            f_str = f_str + f"{f:+8.2f},"
            t_str = t_str + f"{t:+8.2f},"

            sr_val_ar[j] = c_str+"]"+f_str+"]"+t_str[0:-1]+"]"

        # Format names    
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = self.jt_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = self.name+"\n"+full_str+"Action perid: "+str(self.get_act_perid())

        return full_str
    
    def print_table(self,keep_old=False):
        """
        Print message in a table form
        Param keep_old: =True : When scroll up terminal, will see old record
                        =False: No record
        Move curser to origin reference: https://github.com/gravmatt/py-term
        
        """
        hom_pos  = '\033[H'
        clr_str  = '\033[2J'

        if keep_old == True:
            sys.stdout.write(clr_str)

        sys.stdout.write(hom_pos)
        sys.stdout.flush()

        apend_str = self.form_str()
        sys.stdout.write(apend_str)
        sys.stdout.flush()   

    def get_act_perid(self)->float:
        return self.action_perid

    def get_jt_dic(self):
        return self.jt_dic
    
    def get_num_legs(self):
        return self.leg_sz
    
    def get_num_joints(self):
        '''
        Joint size for one leg
        '''
        return self.jont_sz
    
    def get_jont_name(self,jt_idx):
        return self.jt_nam_arr[jt_idx]
    
    def get_leg_name(self,leg_idx):
        return self.jt_dic[leg_idx]["name"]
    
    def get_val_by_idx(self,leg_idx,joint_idx):
        '''
        Given leg index and joint index, return value
        joint_idx: range 0-2
        leg_idx : range 0-5
        '''
        jt_nam = self.jt_nam_arr[joint_idx]
        return self.jt_dic[leg_idx][jt_nam]["val"]


    def get_arr_by_ileg(self,leg_idx)->List[Union[float,float,float]]:
        '''
        Given leg index and return all joints' val as arr
        leg_idx : range 0-5
        return leg_arr: [coxa_val,femur_val,tibia_val]
        '''
        leg_arr = [0]*self.jont_sz

        for joint_idx in range(self.jont_sz):
            jt_nam = self.jt_nam_arr[joint_idx]
            leg_arr[joint_idx] = self.jt_dic[leg_idx][jt_nam]["val"]

        return leg_arr

    def get_jt_dict(self):
        return self.jt_dic
    
    def set_act_perid(self,action_perid:float=0):
        self.action_perid = action_perid

    def set_arr_by_ileg(self,leg_idx:int=0,leg_arr:list=[0,0,0]):
        '''
        Given leg index and return all joints' val as arr
        leg_idx : range 0-5
        leg_arr : [coxa_val,femur_val,tibia_val]
        '''

        for joint_idx in range(self.jont_sz):
            jt_nam = self.jt_nam_arr[joint_idx]
            self.jt_dic[leg_idx][jt_nam]["val"] = leg_arr[joint_idx] 

        return leg_arr


    def set_by_idx(self,leg_idx,joint_idx,joint_val):
        jt_nam = self.jt_nam_arr[joint_idx]
        self.jt_dic[leg_idx][jt_nam]["val"] = joint_val

    def set_by_jt_nam(self,leg_idx,joint_nam,joint_val):
        self.jt_dic[leg_idx][joint_nam]["val"] = joint_val

    def set_all_jt(self,jt_val:float):
        """
        Set all joint to a single value
        """
        for i in range(self.get_num_legs()):
            self.set_arr_by_ileg(i,[jt_val,jt_val,jt_val])
    
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key
        
        '''
        self.jt_dic = self.key_str2int(json_str)    


    def __getitem__(self,idx:int)->List[Union[float,float,float]]:
        """
        Given leg's idx, return [x,y,z]
        """
        if isinstance(idx,int):
            pt_arr = self.get_arr_by_ileg(idx)
            return pt_arr 
        else: 
            print("NotImplemented")
            return NotImplemented

    def __eq__(self,obj):
        """
        type obj: BotJointType
        """

        if isinstance(obj,BotJointType) == False: 
            return False
        
        obj_dic=obj.get_jt_dic()
        for key in self.jt_dic.keys():
            if self.jt_dic[key][self.jt_nam_arr[0]]["val"] != obj_dic[key][self.jt_nam_arr[0]]["val"] or \
               self.jt_dic[key][self.jt_nam_arr[1]]["val"] != obj_dic[key][self.jt_nam_arr[1]]["val"] or \
               self.jt_dic[key][self.jt_nam_arr[2]]["val"] != obj_dic[key][self.jt_nam_arr[2]]["val"]:
                return False
        return True

    def __str__(self):
        return self.form_str()

def test_load_json():
    
    jtdic_tmplt = \
        {
        0: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-middle", "id": 0},
        1: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-front" , "id": 1},
        2: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-front"  , "id": 2},
        3: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-middle" , "id": 3},
        4: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-back"   , "id": 4},
        5: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-back"  , "id": 5}
        }
    
    ct1 = BotJointType()
    ct1.set_by_strkey(jtdic_tmplt)
    jtdic_tmplt = \
        {
        0: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-middle", "id": 0},
        1: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-front" , "id": 1},
        2: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-front"  , "id": 2},
        3: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-middle" , "id": 3},
        4: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "left-back"   , "id": 4},
        5: {"coxa": {"val":0,"mode":"pose"}, "femur": {"val":0,"mode":"pose"}, "tibia": {"val":0,"mode":"pose"}, "name": "right-back"  , "id": 5}
        }
    ct2 = BotJointType()
    ct2.set_by_strkey(jtdic_tmplt)

    print("ct2: \n")
    print(str(ct2))
    ct2.print_table()
    
    print("check equal: "+str(ct1==ct2) )
    print(ct2.check_any_None())
    ct2.set_arr_by_ileg(3,[None,None,None])
    print(ct2.check_any_None())



if __name__ == "__main__":
    test_load_json()