import  sys
sys.path.append("../")

import numpy as np
from    copy                       import deepcopy
from    typing                     import List,Union
from    spatialmath                import SE3
from    custom_type.bot_base_type  import BotBaseType
from    utils.print_flush          import print_flush as print
class BotCartType(BotBaseType):
    __slots__ = ("cart_dic","name"   ,"ct_nam_arr","leg_sz","action_perid"
                 "lft_ids" ,"rht_ids","leg_names" ,"_iter_idx_")

    def __init__(self, name:str="",cart_dic:dict=None):

        self.action_perid = 0

        self.leg_sz    = super().LEG_SZ
        self.lft_ids   = super().LFT_IDS
        self.rht_ids   = super().RHT_IDS
        self.leg_names = super().NAMES_LEG

        # Type check
        if cart_dic is not None: 
            if (isinstance(cart_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')
    
        cart_tmplt = {
            0: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "right-middle","id": 0},
            1: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "right-front" ,"id": 1},
            2: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "left-front"  ,"id": 2},
            3: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "left-middle" ,"id": 3},
            4: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "left-back"   ,"id": 4},
            5: {"x": {"val":0,"mode":"pose"},"y": {"val":0,"mode":"pose"},"z": {"val":0,"mode":"pose"},"name": "right-back"  ,"id": 5}}
        
        self.ct_nam_arr = ["x","y","z"]

        if cart_dic == None:
            self.cart_dic = cart_tmplt
        else: 
            self.cart_dic = deepcopy(cart_dic)

        self.name = name
        
    def increase_by_idx(self,leg_idx:int,cart_idx:int,inc_val:float):
        """
        Increase specify axis by given leg idx, cart_idx, and cart_value
        cart_idx range: 0:x 1:y 2:z
        leg_idx range : leg 0 -- leg 5      
        inc_val: Increase quantity   
        """
        ct_nam = self.ct_nam_arr[cart_idx]
        self.cart_dic[leg_idx][ct_nam]["val"] = self.cart_dic[leg_idx][ct_nam]["val"]+inc_val

    def transf_lft_pts(self,rxyz_deg=[0,0,0],txyz=[0,0,0]):
        """
        Transform left side points
        Rotation is in zyx order 
        """
        R = SE3.RPY(rxyz_deg[0], rxyz_deg[1], rxyz_deg[2],unit="deg", order='zyx')
        T = SE3.Trans(txyz[0],txyz[1],txyz[2])
        transf = T*R

        for id in self.lft_ids:
            x = self.cart_dic[id]["x"]["val"]
            y = self.cart_dic[id]["y"]["val"]
            z = self.cart_dic[id]["z"]["val"]
            arr = transf*[x,y,z]
            self.cart_dic[id]["x"]["val"] = arr[0][0] 
            self.cart_dic[id]["y"]["val"] = arr[1][0]  
            self.cart_dic[id]["z"]["val"] = arr[2][0]  

    def transf_rht_pts(self,rxyz_deg=[0,0,0],txyz=[0,0,0]):
        """
        Transform right side points
        Rotation is in zyx order 
        """
        R = SE3.RPY(rxyz_deg[0], rxyz_deg[1], rxyz_deg[2],unit="deg", order='zyx')
        T = SE3.Trans(txyz[0],txyz[1],txyz[2])
        transf = T*R
        for id in self.rht_ids: 
            x = self.cart_dic[id]["x"]["val"]
            y = self.cart_dic[id]["y"]["val"]
            z = self.cart_dic[id]["z"]["val"]
            arr = transf*[x,y,z]
            self.cart_dic[id]["x"]["val"] = arr[0][0] 
            self.cart_dic[id]["y"]["val"] = arr[1][0]  
            self.cart_dic[id]["z"]["val"] = arr[2][0]  

    def is_all_gnd(self)->bool:
        """
        Check if all legs touch ground (z==0)
        """
        for xyz in self:
            if xyz[2] != 0:
                return False 
        return True


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
        len_legs = len(self.cart_dic)
        sr_val_ar = [""]*len_legs
        # Loop over each row
        for j in range(len_legs):
            x_str = "x: ["
            y_str = " y: ["
            z_str = " z: ["
            x = self.cart_dic[j]["x"]["val"]
            y = self.cart_dic[j]["y"]["val"]
            z = self.cart_dic[j]["z"]["val"]

            x_str = x_str + f"{x:+8.2f},"
            y_str = y_str + f"{y:+8.2f},"
            z_str = z_str + f"{z:+8.2f},"

            sr_val_ar[j] = x_str+"]"+y_str+"]"+z_str[0:-1]+"]"

        # Format names    
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = self.cart_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = "\n"+full_str
        full_str = self.name+full_str+"Action perid: "+str(self.get_act_perid())
        return full_str  
    
    def __iter__(self):
        """
        Reload iterator and return value of x, y, z
        """
        self._iter_idx_ = 0
        return self

    def __next__(self):
        """
        return : [x,y,z]
        """
        if self._iter_idx_ < self.get_num_legs():
            pt = self.get_pt_by_idx(self._iter_idx_)
            self._iter_idx_ += 1
            return pt
        else:
            raise StopIteration
        
    def print_table(self,keep_old=False):
        """
        Print message in a table form
        Param keep_old: =True : When scroll up terminal, will see old record
                        =False: No record
        """

        hom_pos  = '\033[H'
        clr_str  = '\033[2J'

        # Move curser to origin reference: https://github.com/gravmatt/py-term

        if keep_old == True:
            sys.stdout.write(clr_str)

        sys.stdout.write(hom_pos)
        sys.stdout.flush()

        apend_str = self.form_str()
        sys.stdout.write(apend_str)
        sys.stdout.flush()      
        
    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls    = self.__class__
        result = cls.__new__(cls)

        # copy value 
        result.cart_dic   = deepcopy(self.cart_dic  )
        result.ct_nam_arr = deepcopy(self.ct_nam_arr)
        result.name       = self.name
        result.leg_sz     = self.leg_sz
        result.lft_ids    = self.lft_ids
        result.rht_ids    = self.rht_ids
        result.leg_names  = self.leg_names
        result.action_perid  = self.action_perid

        return result

    def mat_dot_self(self,trans:SE3):
        """
        Given translation matrix , update legs' points respectively 
        e.g: tran_cob*T_right-middle
             tran_cob*T_right-front
             tran_cob*T_left-front
             ...

        Param : tran_cob: Given tans matrix
        return: Transformed BotCartType object
        """

        result = self.clone()
        # Translate matrices
        for key in range(self.leg_sz):
            cat_arr = trans*self.get_pt_by_idx(key)
            result.set_by_leg_idx(key,[cat_arr[0][0],cat_arr[1][0],cat_arr[2][0]])

        # copy value 
        result.name = "trans from " +self.name+": "
        return result

    def get_act_perid(self)->float:
        return self.action_perid

    def get_leg_names(self,idx:int)->str:
        leg_nam = self.leg_names[idx]
        return leg_nam

    def get_num_legs(self)->int:
        return self.leg_sz
    
    def set_mode_by_idx(self,leg_idx:int,cart_idx:int,mode:str):
        '''
        leg_idx : range 0-5   map to leg 0-5
        axis_idx: range 0,1,2 map to x,y,z
        '''
        ct_nam = self.ct_nam_arr[cart_idx]
        self.cart_dic[leg_idx][ct_nam]["mode"] = mode
        
    def set_mode_by_leg_idx(self,leg_idx:int,mode=["pose","pose","pose"]):
        '''
        leg_idx : range 0-5   map to leg 0-5
        axis_idx: range 0,1,2 map to x,y,z
        '''
        for cart_idx in range(3):
            ct_nam = self.ct_nam_arr[cart_idx]
            self.cart_dic[leg_idx][ct_nam]["mode"] = mode[cart_idx]

    def get_mode_by_leg_idx(self,leg_idx:int)->List[Union[str,str,str]]:
        '''
        leg_idx : range 0-5   map to leg 0-5
        '''
            
        mode_arr = []
        for cart_idx in range(3):
            ct_nam = self.ct_nam_arr[cart_idx]
            mode_arr.append(self.cart_dic[leg_idx][ct_nam]["mode"])
        return mode_arr
    
    def get_mode_by_idx(self,leg_idx:int,cart_idx:int=None)->str:
        '''
        leg_idx : range 0-5   map to leg 0-5
        axis_idx: range 0,1,2 map to x,y,z
        '''

        ct_nam = self.ct_nam_arr[cart_idx]
        return self.cart_dic[leg_idx][ct_nam]["mode"]
    
    def get_pt_by_idx(self,leg_idx:int)->List[Union[float,float,float]]:
        '''
        param leg_idx : range 0-5
        return        : [x,y,z]
        '''
        ct_x = self.ct_nam_arr[0]
        ct_y = self.ct_nam_arr[1]
        ct_z = self.ct_nam_arr[2]

        x = self.cart_dic[leg_idx][ct_x]["val"]
        y = self.cart_dic[leg_idx][ct_y]["val"]
        z = self.cart_dic[leg_idx][ct_z]["val"]

        return [x,y,z]
    


    def get_by_idx(self,leg_idx:int,cart_idx:int):
        '''
        leg_idx : range 0-5   map to leg 0-5
        axis_idx: range 0,1,2 map to x,y,z
        '''
        ct_nam = self.ct_nam_arr[cart_idx]
        return self.cart_dic[leg_idx][ct_nam]["val"]
    
    def get_ct_dict(self):
        return self.cart_dic
    
    def set_act_perid(self,action_perid:float=0):
        self.action_perid = action_perid
        
    def set_by_leg_idx(self,leg_idx:int,cat_arr:List[Union[float,float,float]]):
        '''
        Set pose by given leg tip corrdinate and leg index 
        leg_idx range: 0 --5 
        cat_arr size: 3
        '''
        ct_nam_x = self.ct_nam_arr[0]
        ct_nam_y = self.ct_nam_arr[1]
        ct_nam_z = self.ct_nam_arr[2]
        self.cart_dic[leg_idx][ct_nam_x]["val"] = cat_arr[0]
        self.cart_dic[leg_idx][ct_nam_y]["val"] = cat_arr[1]
        self.cart_dic[leg_idx][ct_nam_z]["val"] = cat_arr[2]
     
    def set_by_idx(self,leg_idx:int,cart_idx:int,cart_val:float): 
        '''
        Set specify axis by given leg idx, cart_idx, and cart_value
        cart_idx range: 0:x 1:y 2:z
        leg_idx range : leg 0 -- leg 5 
        '''
        ct_nam = self.ct_nam_arr[cart_idx]
        self.cart_dic[leg_idx][ct_nam]["val"] = cart_val

    def set_by_ct_nam(self,leg_idx:int,cart_nam:str,cart_val:float):
        '''
        leg_idx range: 0 --5 
        Choices for  cart_nam are: "x","y","z"
        '''
        self.cart_dic[leg_idx][cart_nam]["val"] = cart_val

    def set_by_strkey(self,json_str:dict):
        '''
        Json file does not support int key, Convert to int key
        
        '''
        self.cart_dic = self.key_str2int(json_str)   

    def set_name(self,name:str):
        self.name = name 
        

    def __rmul__(self,tran:SE3):
        """
        Given translation matrix from gnd to cob, update hexagon coordinates respectively 
            e.g: 
                leg_pts     = BotCartType("hgd")
                mat_gnd2cob = SE3.Trans(0,0,10)
                pts_gnd2bdy = mat_gnd2cob*leg_pts
        Param : tran: Given tans matrix
        return: Transformed BotCartType object
        """

        if isinstance(tran,SE3): 
            result = self.mat_dot_self(tran)
            return result
        else:
            return NotImplemented 

    def __iter__(self):
        self._iter_idx_ = 0
        return self    
    
    def __next__(self)->List[Union[float,float,float]]:
        if self._iter_idx_ < self.get_num_legs():
            [x,y,z] = self[self._iter_idx_]
            self._iter_idx_ += 1
            return [x,y,z]
        else:
            raise StopIteration
    
    def __sub__(self,robj)->float:
        """
        Return l2_norm average for all legs
        """
        l2_abs_dis = 0
        if isinstance(robj,BotCartType): 
            for i,pt in enumerate(robj):
                l2_norm = np.linalg.norm(np.array(self[i])-np.array(pt))
                l2_abs_dis = l2_abs_dis+l2_norm
            l2_avg = l2_abs_dis/self.get_num_legs()
            return l2_avg

        else:
            return NotImplemented 

    def __eq__(self, robj)->bool:
        if isinstance(robj,BotCartType): 
            for i,pt in enumerate(robj):
                if self[i] != pt:
                    return False
            return True
        else:
            return NotImplemented 

    def __len__(self):
        """
        Get number of legs 
        """
        return self.get_num_legs()

    def __getitem__(self,idx:int)->List[Union[float,float,float]]:
        """
        Given leg's idx, return [x,y,z]
        """
        if isinstance(idx,int):
            pt_arr = self.get_pt_by_idx(idx)
            return pt_arr 
        else: 
            print("NotImplemented")
            return NotImplemented

    def __str__(self):
        full_str = self.form_str()
        return full_str     


def test_loop():
    dic_tmplt = \
        {
        0: {"x": {"val":1 ,"mode":"pose"},"y": {"val":2 ,"mode":"pose"},"z": {"val":3 ,"mode":"pose"},"name": "right-middle","id": 0},
        1: {"x": {"val":12,"mode":"pose"},"y": {"val":22,"mode":"pose"},"z": {"val":32,"mode":"pose"},"name": "right-front" ,"id": 1},
        2: {"x": {"val":13,"mode":"pose"},"y": {"val":23,"mode":"pose"},"z": {"val":33,"mode":"pose"},"name": "left-front"  ,"id": 2},
        3: {"x": {"val":14,"mode":"pose"},"y": {"val":24,"mode":"pose"},"z": {"val":34,"mode":"pose"},"name": "left-middle" ,"id": 3},
        4: {"x": {"val":16,"mode":"pose"},"y": {"val":26,"mode":"pose"},"z": {"val":36,"mode":"pose"},"name": "left-back"   ,"id": 4},
        5: {"x": {"val":17,"mode":"pose"},"y": {"val":27,"mode":"pose"},"z": {"val":37,"mode":"pose"},"name": "right-back"  ,"id": 5}
        }
        
    ct1 = BotCartType("ct1",dic_tmplt)
    
    for ptxyz in ct1:
        print("ptxyz: ",ptxyz)
    # ctt = SE3.Trans(4,5,6)*ct1
    # ctr = SE3.RPY([10,0,0],unit="deg",order='zyx')*ct1
    # print(ctr)
    # print(ctt.get_num_legs())

    # for i,pt in enumerate(ctr):
    #     print(i,pt)
    # print(ctr == ct1)

if __name__ == "__main__":

    test_loop()