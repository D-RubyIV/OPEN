


class AllBody():
    def __init__(self) -> None:
        self.firstBody = open("Data\PhanDau.txt","r", encoding="utf-8").read()
        self.secondBody = open("Data\PhanThan.txt","r", encoding="utf-8").read()
        self.thirdBody = open("Data\PhanCuoi.txt","r", encoding="utf-8").read()

    def getAllBody(self):
        text = ""
        text += self.firstBody + "\n"
        text += self.secondBody + "\n"
        text += self.thirdBody + "\n"
        return text
