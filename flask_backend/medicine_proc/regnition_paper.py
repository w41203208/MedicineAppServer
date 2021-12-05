import time


class RegPre():
    def __init__(self):
        self.data = dict()

    def preRecognize(self):
        time.sleep(7)

        self.data ={
            '0' : {
                "p_medicineName" : [
                    {
                        "name" : "Alat",
                        "predict" : 0.9
                    },
                    {
                        "name" : "Alaatat",
                        "predict" : 0.7
                    },
                    {
                        "name" : "Alattt",
                        "predict" : 0.4
                    },
                    {
                        "name" : "Alaaaatt",
                        "predict" : 0.1
                    },
                ],
                "p_medicineNum" : 14,
            },
        }
        reg = 'pre'

        return self.data, reg




