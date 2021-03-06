
class Category:
    def __init__(self,name,depth):
        self.cat_name=name
        self.depth=depth
        self.subcategories=[]

    def GetName(self):
        return self.cat_name

    def find_sub(self,name,depth):
        if depth==self.depth+1:
            for sub_cat in self.subcategories:
                if sub_cat.GetName() == name:
                    return sub_cat
        result=None
        if depth>self.depth+1:
            for sub_cat in self.subcategories:
                if not sub_cat.find_sub(name,depth) is None:
                    return sub_cat

        return None

    def add_sub(self,name,depth):
        if depth==self.depth+1:
            self.subcategories.append(Category(name,depth))
        else:
            self.subcategories[len(self.subcategories)-1].add_sub(name,depth)

    def textify(self):
        result=""
        for i in range(self.depth):
            result+="#"

        return result+self.cat_name


    def __str__(self):
        result=""
        result+=self.textify()+"\n"
        for sub_cat in self.subcategories:
            result+=sub_cat.__str__()
        return result

class File_Processor:
    def __init__(self,filename):
        self.filename=filename

    def get_rest_of_line(self,position,data):
        result=""
        while position<len(data) and data[position]!="\n":
            result+=data[position]
            position+=1
        return result,position

    def AddForm(self,title,alternatives,categories):
        file=open(self.filename,"a")
        file.write("!"+title+"\n")
        for alt in alternatives:
            file.write("@"+alt+"\n")
        for cat in categories:
            file.write(cat.__str__())
        file.close()

    def RemoveForm(self,title):
        file=open(self.filename,"r")
        file_data=file.read(-1)
        file.close()
        start_position,end_position,position=(-1,-1,0)
        title_found=False
        while (position < len(file_data)):
            if file_data[position] == "!":
                if title_found:
                    end_position=position
                    break
                else:
                    start_position=position
                position+=1
                found_title, position = self.get_rest_of_line(position, file_data)
                if found_title==title:
                    title_found=True
            position+=1
        result=file_data[:start_position]+file_data[end_position:-1]
        file=open(self.filename,"w")
        file.write(result)
        file.close()

    def TakeForm(self,title):
        file=open(self.filename,"r")
        file_data=file.read(-1)
        position=0
        alternatives=[]
        categories=[]
        while(position<len(file_data)):
            if file_data[position]=="!":
                position+=1
                found_title,position=self.get_rest_of_line(position,file_data)
                if found_title==title:
                    position+=1
                    while position<len(file_data) and file_data[position]=="@":
                        position+=1
                        alt,position=self.get_rest_of_line(position, file_data)
                        alternatives.append(alt)
                        position+=1
                    while position<len(file_data) and file_data[position]=="#":
                        depth=0
                        while file_data[position]=="#":
                            depth+=1
                            position+=1
                        if depth==1:
                            cat,position=self.get_rest_of_line(position, file_data)
                            categories.append(Category(cat,1))
                            position+=1
                        else:
                            cat,position=self.get_rest_of_line(position, file_data)
                            categories[len(categories)-1].add_sub(cat,depth)
                            position+=1
                    if position<len(file_data) and file_data[position]=="!":
                        position-=1
            position+=1
        file.close()
        return (alternatives,categories)

    def CheckForms(self):
        file=open(self.filename)
        file_data=file.read(-1)
        position=0
        titles=[]
        while (position < len(file_data)):
            if file_data[position] == "!":
                position += 1
                found_title, position = self.get_rest_of_line(position, file_data)
                titles.append(found_title)
            position += 1
        file.close()
        return titles

if __name__ == '__main__':
    processor=File_Processor("test.txt")
    #taken_alt,taken_cat=processor.TakeForm("Bruh")
    #print(taken_alt)
    #print(taken_cat)
    #print(processor.CheckForms())
    test_cat=[]
    test_cat.append(Category("test1",1))
    test_cat[0].add_sub("test1.1",2)
    test_cat[0].add_sub("test1.2", 2)
    test_cat.append(Category("test2", 1))
    test_cat.append(Category("test3", 1))
    # processor.AddForm("Bruh2",["a","b","bazinga"],test_cat)
    processor.RemoveForm("Bruh")
