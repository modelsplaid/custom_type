
import sys 
import json
sys.path.append("./")

from    copy                      import deepcopy
from    typing                    import List,Union

from custom_type.walk_dir_type    import WalkDirType
from custom_type.gait_seqs_type   import GaitIdxSeqsType
from custom_type.gait_props_type  import GaitPropsType
from custom_type.ik_props_type    import IKPropsType

import custom_type

print(custom_type.gait_seqs_type.__file__)

class WalkCfgType(WalkDirType):

    __slots__ = ("walk_cfg_dic","_iter_idx_")

    def __init__(self,walk_cfg_dic:dict=None):
        super().__init__('walkingforward')
        
        walk_cfg_tmplt = {
            "walkingforward" : GaitIdxSeqsType(),"walkingbackward": GaitIdxSeqsType(),
            "rotatingleft"   : GaitIdxSeqsType(),"rotatingright"  : GaitIdxSeqsType(),
            "BDY_IK_PARAMS"  : IKPropsType(),"GAITS_PROPS_CFG": GaitPropsType(),
        }
        
        self.walk_cfg_dic =  walk_cfg_tmplt
        
        if walk_cfg_dic == None:
            self.walk_cfg_loader()
        else: 
            self.set_walk_cfg_dic(walk_cfg_dic)
    
    def walk_cfg_loader(self,act_sqs_fil:str="./custom_type/test/walk1_cfg.json"):

        out_file    = open(act_sqs_fil, "r")
        act_sqs_dic = json.load(out_file)
        self.set_walk_cfg_dic(act_sqs_dic)
        
    def set_walk_cur_dir_idx(self,idx:int):
        """
        Set current direction
        0:'walkingforward' ,1:'walkingbackward',2: 'rotatingleft',3: 'rotatingright'
        """
        if idx < 0 or idx >= len(self.WLK_LST):
            raise IndexError('fatal error: Incorrect arguments index')
        self.set_cur_dir_idx(idx)
        
    def set_walk_cfg_dic(self,act_sqs_dic:dict=None):
        """
        Action of legs and valve-pumps type: 
        Examples: Seen in walk1_cfg.json
        """
        self.walk_cfg_dic["walkingforward" ] = GaitIdxSeqsType(act_sqs_dic["CTRAJ_IDX_SEQS_FWD" ],"fordward sqs")
        self.walk_cfg_dic["walkingbackward"] = GaitIdxSeqsType(act_sqs_dic["CTRAJ_IDX_SEQS_BKD" ],"backward sqs")
        self.walk_cfg_dic["rotatingleft"   ] = GaitIdxSeqsType(act_sqs_dic["CTRAJ_IDX_SEQS_ROTL"],"rotate left sqs")
        self.walk_cfg_dic["rotatingright"  ] = GaitIdxSeqsType(act_sqs_dic["CTRAJ_IDX_SEQS_ROTR"],"rotate right sqs")
        self.walk_cfg_dic["BDY_IK_PARAMS"  ] = IKPropsType    (act_sqs_dic["BDY_IK_PARAMS"      ],"body ik params")
        self.walk_cfg_dic["GAITS_PROPS_CFG"] = GaitPropsType  (act_sqs_dic["GAITS_PROPS_CFG"    ],"gaits props")
    def get_gaits_props(self)->GaitPropsType:
        """
        Get gait properties
        """
        return deepcopy(self.walk_cfg_dic["GAITS_PROPS_CFG"])
    
    def get_bdy_ik_props(self)->IKPropsType:
        """
        Get body ik properties
        """
        return deepcopy(self.walk_cfg_dic["BDY_IK_PARAMS"])
    
    def get_cur_dir_sqs_len(self)->int:
        """
        Get length of gait sequence
        """
        return self.get_current_acts().get_sqs_len()
    
    def get_current_acts(self)->GaitIdxSeqsType:
        cur_dir = self.get_cur_dir()
        return deepcopy(self.walk_cfg_dic[cur_dir])
        
    def get_fwd_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.walk_cfg_dic[self.WLK_FWD])

    def get_bak_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.walk_cfg_dic[self.WLK_BKWD])
    
    def get_rotl_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.walk_cfg_dic[self.ROT_LFT])
    
    def get_rotr_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.walk_cfg_dic[self.ROT_RHT])
    
    def get_acts_by_idx(self,idx:int)->GaitIdxSeqsType:
        dir_nam = self.WLK_LST[idx%len(self.WLK_LST)]
        return deepcopy(self.walk_cfg_dic[dir_nam])

    def get_acts_by_nam(self,dir_nam:WalkDirType)->GaitIdxSeqsType:
        cta = deepcopy(self.walk_cfg_dic[dir_nam.get_cur_dir()])
        return cta
    
    def __iter__(self):
        self._iter_idx_ = 0
        return self
    
    def __next__(self)->GaitIdxSeqsType:
        if self._iter_idx_ < len(self.WLK_LST):
            cta = self.get_acts_by_idx(self._iter_idx_)
            self._iter_idx_ += 1
            return cta
        else:
            raise StopIteration
        
        
if __name__ == "__main__":
    acq = WalkCfgType()
    print(acq.walk_cfg_dic["walkingforward"].get_sqs_len())
    print("bdy ik: \n", str(acq.get_bdy_ik_props()))
    print("gaits props: \n", str(acq.get_gaits_props()))
    print("dir: ", acq.get_cur_dir())
    print("current dir: ", acq.get_cur_dir())
    # todo: here
    
    # acq.set_cur_dir_idx(3)
    # print(acq.get_current_acts())
    # print(acq.get_cur_dir())
    # print(acq.get_acts_by_idx(0))
    # for idx,act in enumerate(acq):
    #    print(idx,act,"\n------\n")