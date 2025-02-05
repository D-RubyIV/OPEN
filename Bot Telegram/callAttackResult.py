


class CallBookmaker():

    def __init__(self, stringResult):
        self.stringResult = stringResult
        with open("Data\CongThuc.txt", "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            listCongThuc  = list(filter(None, lines))  #
        self.congThuc = sorted(listCongThuc, key=lambda x: len(x))
        print(self.congThuc)


    def convert_string(self, s):
        result = ""
        s = s.split("_")[0]
        for i in range(len(s)):
            if s[i].isdigit():
                for j in range(int(s[i])-1):
                    result += s[i+1].upper()
            elif s[i].isalpha():
                result += s[i].upper()
        return result


    def callResult(self):
        print(f"From Result: {self.stringResult}")
        listKQ = []
        for congThuc in self.congThuc:
            kqTraVe = congThuc.split("_")[1]
            chuoiCongThuc = congThuc.split("_")[0]
            KQBook = self.convert_string(chuoiCongThuc)
            if self.stringResult[:len(KQBook)] == KQBook:
                print("Khớp Công Thức: " + chuoiCongThuc + " ==> Result: " + kqTraVe)
                listKQ.append(kqTraVe.strip())
        return listKQ[-1]
            

