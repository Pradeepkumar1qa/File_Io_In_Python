import  os
import sqlite3
from sqlite3 import Error

#comment added to see merge conflict
root_path_of_project="C:"+os.environ['HOMEPATH']+'\\Desktop\\px_17_feb\\PXSelenium\\dbmapperconfig.txt'
print(root_path_of_project)

path_for_package="C:\\Users\\Pradeep Kumar\\Desktop\\px_17_feb\\PXSelenium\\src\\test\\java\\"
path_for_sql_file="C:\\Users\\Pradeep Kumar\\Desktop\\px_17_feb\\PXSelenium\\"









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
    """
    will return a dictionary having key as function name and value is all those test case id in stiring format which is mapped
    to this particular funciton name.
    for example {"test_step_1":'"tcid_1","tcid_2"'}
    :param filename: filename is the name of file or classname for which dictionary  will be build
    :param dbpath: path of sqlite file
    :return: a Dictionary having function name as key and all those test case id which is mapped to this method as value
    """
    sql='select * from '+filename;
    #print(sql)
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
            testcaseid=str(row[tcid]).replace("\n","")
            if dic.keys().__contains__(row[teststep]):
                dic[row[teststep]] = dic[row[teststep]] + ',' + '"' + testcaseid + '"'
            else:
                dic[row[teststep]] = '"' + str(testcaseid) + '"'
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



def modify_content(filename,dic,path_for_package):
      """
      will modify the content as per the mapping.will add a line @Dbmapper(testcasdid="") to funciton which is allready mapped to some id
      :param filename: Name of file or class for which mapping is to be done
      :param dic: dictionary having the key as function  name and value as all those test case id which is mapped to key function
      :return: return a modified list after doing mapping of the function
      """
      funname=''
      path=path_for_package+'\\'+filename
      with open(path,'r',encoding="utf8") as fr:
          l=fr.readlines()
          # print(l);
          counter=0

          for i in range(len(l)):

               if l[i].lstrip().startswith("@Test"):
                        counter=i;
                        while not (l[counter].lstrip().startswith('public void')):
                             counter=counter+1
                        funname=getName(l[counter])

                        #print(funname+"_pradeep")
                        while not (l[counter].lstrip().startswith("@DbMapper") or  l[counter].lstrip().endswith('}') or l[counter].lstrip().startswith('}')):
                            counter=counter-1
                           # print(counter,l[counter] ,not (l[counter].lstrip().startswith("@DbMapper") or  l[counter].lstrip().endswith('}') or l[counter].lstrip().endswith('}')))
                        if l[counter].lstrip().startswith("@DbMapper"):
                            #print(l[counter]+"pradeep")
                            l[counter]=""

                        if funname in dic.keys():
                                # print('found method'+funname+"")
                                l[i] = '\t@DbMapper(testcaseid={' + dic[funname] + '})\n' + l[i]
                                # print(l[i])




          return l;


# l=modify_content("Quiz_With_Existing_Created_Multiple_Answer_Question_Test.java",dic)
# print(l)

def write_content(filename,l,path_for_package):
    """
    will write the content in file name after modification of content
    :param filename: filename for which the mapping is going to be done
    :param l: list of modified content
    :return: Void
    """
    counter=0;
    path=path_for_package+"\\"+filename
    with open(path,'w',encoding="utf8") as fw:
        for s in l:
            if(counter==1  and not (l[1].__contains__('import com.qait.annotation.DbMapper;'))):
                fw.write("import com.qait.annotation.DbMapper;\n")
            fw.write(s)
            counter=counter+1;
        fw.flush()

def remove_dbMapper_And_build_content(filename):
        """
        to support backward compatibility in case of any failure we need to remove all those dbmapper annotation from the file
        :param filename:
        :return:
        """
        path = path_for_package+"\\"+filename
        with open(path, 'r') as fr:
            l = fr.readlines();
            # print(l);
            counter = 0

            for i in range(len(l)):
                if l[i].lstrip().startswith("@DbMapper"):
                  l[i]="";
            return l;


# write_content("Quiz_With_Existing_Created_Multiple_Answer_Question_Test.java",l)


def write_annotation_to_all_those_step_which_is_all_ready_mapped(path_for_package,path_for_sql_file,flag=True):
    """
    method will do the processing based on the flag parameter set if flag=True (default value) will annotated the method
    and flag=False will remove all the dbmapper annotation from the function make the function original one
    :param flag: default is True in order to remove the annotation you will have to make it False;
    :return: Void
    """
    print("starting mapping for ")
    for subdir, dirname, file in os.walk(path_for_package):
        path = path_for_sql_file
        l=[]
        print(file)
        for f in file:
            dic = db_getmappingsforclass(f.replace('.java', ""), path)
            print(f,dic)
            #print("*******************************************************************")
            if len(dic.keys()) == 0: continue
            if(flag):
                l = modify_content(f, dic,path_for_package)
            elif not flag:
                l = remove_dbMapper_And_build_content(f)
            #print(l)
            write_content(f, l,path_for_package)
            print("processing done for \t "+f)


            # print(f+"done");



def divider():
    print("-*-"*30)

def set_path_for_pacakage_and_sql_file_by_looking_dbmapperconfig_file():
    global path_for_sql_file,path_for_package


    current_path_for_package= path_for_package
    current_path_for_sql_file=path_for_sql_file
    print(current_path_for_sql_file)
    print(current_path_for_package)
    #exit(0)
    with open(root_path_of_project) as f:
        l=f.readlines();
    for individual_line in l:
        list_containing_info_for_package_and_sql=individual_line.split("-")
        path_for_package=(current_path_for_package.lstrip()+list_containing_info_for_package_and_sql[1].replace('.',"\\").strip()).strip()
        path_for_sql_file=(current_path_for_sql_file.lstrip()+list_containing_info_for_package_and_sql[2].replace('\n',"").strip()).strip()
        divider()
        print("package name:\t"+path_for_package)
        print("sql file location:\t"+path_for_sql_file)
        #print(path_for_package)
        # for root,subdir,file in os.walk(path_for_package.strip()):
        #     print(file)
        write_annotation_to_all_those_step_which_is_all_ready_mapped(path_for_package,path_for_sql_file)



set_path_for_pacakage_and_sql_file_by_looking_dbmapperconfig_file()
