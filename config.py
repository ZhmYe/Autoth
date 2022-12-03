class Config:
    def __init__(self):
        self.config = [
            {
                "gpu": 1,
                "cpu": 6,
                "memory": 60
            },
            {
                "gpu": 2,
                "cpu": 12,
                "memory": 120
            },
            {
                "gpu": 0,
                "cpu": 1,
                "memory": 5
            },
            {
                "gpu": 0,
                "cpu": 6,
                "memory": 30
            },
            {
                "gpu": 0,
                "cpu": 12,
                "memory": 60
            },
            {
                "gpu": 0,
                "cpu": 36,
                "memory": 180
            },
        ]
    def choose(self, index):
        return self.config[index]
    def print(self):
        print("-------------------Config-------------------")
        for index in range(len(self.config)):
            config = self.config[index]
            print("{}:      gpu: {}, cpu: {}, memory: {}".format(index, config["gpu"], config["cpu"], config["memory"]))
        print("-------------------Config End-------------------\n\n")