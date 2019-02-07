import  os
import sqlite3
from sqlite3 import Error

#comment added to see merge conflict


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def db_getmappingsforclass(filename,dbpath):
    sql='select * from '+filename;
    print(sql)
    dic = {}
    try:
        conn=create_connection(dbpath)
        cor=conn.cursor()
        cor.execute(sql)
        names = [description[0] for description in cor.description]

        rows = cor.fetchall()
        teststep=0;
        tcid=1
        issue=2
        teststep=names.index("teststep")
        tcid=names.index("tcid");
        for row in rows:

            if dic.keys().__contains__(row[teststep]):
                dic[row[teststep]] = dic[row[teststep]] + ',' + '"' + row[tcid] + '"'
            else:
                dic[row[teststep]] = '"' + row[tcid] + '"'
    except Error as e:
        print(e)

    return dic



# print(dic)
# for k in dic.keys():
#     print(k+"*********"+dic[k])



def getName(line):
    temp=line.strip().split(" ")[2]
    temp=temp.replace('(',"")
    temp=temp.replace(')',"")
    temp=temp.strip();
    # print(temp)
    return temp;



def modify_content(filename,dic):

      funname=''
      path='C:\\Users\\Pradeep Kumar\\Desktop\\testdata\\'+filename
      with open(path,'r') as fr:
          l=fr.readlines();
          # print(l);
          counter=0

          for i in range(len(l)):
               if l[i].lstrip().startswith("@Test"):
                        counter=i;
                        while not (l[counter].lstrip().startswith('public void')):
                             counter=counter+1
                        funname=getName(l[counter])
                        #print(funname+"_pradeep")
                        if funname in dic.keys():
                            print('found method'+funname+"")
                            l[i]='@Dbmapper(testcaseid={'+dic[funname]+'})\n'+l[i]


          return l;


# l=modify_content("Quiz_With_Existing_Created_Multiple_Answer_Question_Test.java",dic)
# print(l)

def write_content(filename,l):
    path='C:\\Users\\Pradeep Kumar\\Desktop\\testdata\\'+filename
    with open(path,'w') as fw:
        for s in l:
            fw.write(s)


# write_content("Quiz_With_Existing_Created_Multiple_Answer_Question_Test.java",l)
for subdir, dirname, file in os.walk("c:\\Users\\Pradeep kumar\\Desktop\\testdata"):
    path = 'C:\\Users\\Pradeep Kumar\\Desktop\\database\\qpv1.sq3'

    print(file)
    for f in file:
        dic = db_getmappingsforclass(f.replace('.java',""), path)
        print(dic)
        #print("*******************************************************************")
        if len(dic.keys())==0:continue
        l = modify_content(f,dic)
        #print(l)
        write_content(f,l)
        #print(f+"done");



