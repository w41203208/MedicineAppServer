import time


class RegMed():
    def __init__(self):
        self.data = dict()

    def regMedicine(self):
        time.sleep(1)
        self.data ={
            '0' : {
                "r_medicineName" : "testtesttest123",
                "r_medicineNum" : 20,
            },
            '1' : {
                "r_medicineName" : "yyssyy123",
                "r_medicineNum" : 32,
            },
        }

        reg = 'med'

        return self.data, reg