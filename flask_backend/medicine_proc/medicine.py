import json, time
from .regnition_paper import RegPre
from .regnition_drug import excute
from flask_socketio import emit



class MedicineApp():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        self.regpre = RegPre()
        #self.regmed = RegMed()
        self.selectDict = {}
        self.drugDict = {}

    def getPreReg(self):
        pre_data, reg = self.regpre.preRecognize()
        return pre_data

    def getMedReg(self, cap):
        med_data = excute(cap)
        self.drugDict = med_data
        return med_data

    def compare(self, drug_dict, select_dict):

        temp_arr = []
        for i in range(len(drug_dict)):
            if (drug_dict[i]['drug_name'] == select_dict[i]['paper_name']) and drug_dict[i]['drug_quality'] == select_dict[i]['paper_num']:
                temp_arr.append({
                    'result_name' : select_dict[i]['paper_name'],
                    'result_num' : drug_dict[i]['drug_quality'],
                    'result_accuracy' : True,
                })
            else:
                temp_arr.append({
                    'result_name' : select_dict[i]['paper_name'],
                    'result_num' : drug_dict[i]['drug_quality'],
                    'result_accuracy' : False,
                })

        return temp_arr

    #未實現
    def setSelectDict(self, dict):
        self.selectDict = dict
    def getSelectDict(self):
        return self.selectDict




