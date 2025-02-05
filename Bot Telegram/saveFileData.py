


class SaveDataWinLose():
    def __init__(self, text) -> None:
        self.text = text
    def saveData(self):
        my_list = open("Data\PhanThan.txt","r",encoding="utf-8").readlines()
        with open("Data\PhanThan.txt","w+",encoding="utf-8") as f:
            if len(my_list) >= 30:
                my_list.pop(0)
            
            for item in my_list:
                f.write(item)
            f.write("\n" + self.text)
            


           

