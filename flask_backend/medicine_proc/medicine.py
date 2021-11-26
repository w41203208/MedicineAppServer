import json, time
from .regnition_paper import RegPre
from .regnition_drug import excute
from flask_socketio import emit



'''
class ProgressSocket():
    # 建構式
    def __init__(self, socketio=None, socket_id=""):
        self.progress = 0                          # [進度條] 初始進度
        self.socketio = socketio                     # [進度條] socketio連線實體
        self.socket_id = socket_id

    # 利用Socket推送進度
    def emit(self, step,  data, reg, increase):
        #if (step-1)*0.25 > self.progress: self.progress = (step-1)*0.25
        #self.progress += increase
        self.progress += increase
        print(self.progress)
        emit('response', {
            'step' : step,
            'data' : data,
            'reg' : reg,
            'increase' : increase
        },room=self.socket_id)


class Medicine():
    def __init__(self, progress=None):
        self.progress = progress
        self.regpre = RegPre()
        self.regmed = excute()

    def emit_prg(self, step,  data, reg, increase):
        if self.progress!=None:
            self.progress.emit(step,  data, reg, increase)

    def process(self):

        pre_data, reg = self.regpre.preRecognize()
        emit('response', {
            'step' : 1,
            'data' : pre_data,
            'reg' : reg,
            'increase' : 40
        })
        #self.emit_prg(1, pre_data, reg, 40)

        med_data, reg = self.regmed.regMedicine()
        emit('response', {
            'step' : 2,
            'data' : med_data,
            'reg' : reg,
            'increase' : 40
        })
        #self.emit_prg(2, med_data, reg, 40)


        return pre_data, med_data
'''


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




