# coding: utf-8
import pandas as pd
import glob

trans={
    "Y":"永久",
    "D30":"30年",
    "D10":"10年",
    "10年":"D10",
    "30年":"D30",
    "永久":"Y"
}#帮助识别文件路径，目前没啥用



#J004-WS·2022·Y-0001
#J011-WS·2021-D10-0286
#J001-2013-永久-434
def data_rule(item,line,error):
    need_list=["全宗号","档案门类","年度","保管期限","件号"]
    temp=False
    for i in need_list:#必要字段是否存在
        if pd.isnull(item["档号"]):
            error.append((str(file)+" 第"+str(line+2)+"行","","档号为空"))
            return False
        elif pd.isnull(item[i]):
            temp=True
            error.append((str(file)+" 第"+str(line+2)+"行",item["档号"],i+"关键字为空"))
    if temp:
        return False
    if((item["档号"]==(str(item["全宗号"])+"-"+str(item["档案门类"])+"·"+str(item["年度"])+"·"+str(item["保管期限"])+"-"+str(item["件号"]))) and int((item["年度"]))>=2022) or ((item["档号"]==(str(item["全宗号"])+"-"+str(item["档案门类"])+"·"+str(item["年度"])+"-"+str(item["保管期限"])+"-"+str(item["件号"]))) and int((item["年度"]))<=2021 and int((item["年度"]))>=2017) or ((item["档号"]==(str(item["全宗号"])+"-"+str(item["年度"])+"-"+str(item["保管期限"])+"-"+str(item["件号"]))) and int((item["年度"]))<=2016):
        #相应的档号规范设置
        return True
    else:
        error.append((str(file)+" 第"+str(line+2)+"行",item["档号"],"档号命名不规范"))
        return False

def start(sheet,pdfPath,error):
    # 输出多个 Sheet

    for i in sheet.keys():
        if not sheet[i].empty:
            for j in sheet[i].index:
                if data_rule(sheet[i].loc[j],j,error):
                    if len(glob.glob('**/'+str(sheet[i]["档号"].at[j])+'.pdf',root_dir=pdfPath,recursive=True))>0:#查找是否有该文件
                        pass
                    else:
                        if not (trans[str(sheet[i]["保管期限"].at[j])]=="D10" or str(sheet[i]["保管期限"].at[j])=="D10"):#十年期限的文件无需有扫描件
                            error.append((str(file)+" 第"+str(j+2)+"行",str(sheet[i]["档号"].at[j]),"文件不存在或文件名与档号不同"))



def dataCheck(FILE_PATH):
    error=[]
    try:
        file = FILE_PATH.split('\\')[-1]
        if FILE_PATH:
            sheet = pd.read_excel(FILE_PATH, sheet_name=None,index_col=None,dtype={'件号': str,"年度":str,"档案门类":str,"保管期限":str})
            # 输出多个 Sheet
            for i in sheet.keys():
                if not sheet[i].empty:
                    for j in sheet[i].index:
                        data_rule(sheet[i].loc[j],j,error)
    except Exception as e:
        print(e)

    return error
file=""
def pdfFileCheck(FILE_PATH,PDF_PATH):
    error = []
    file = FILE_PATH.split('\\')[-1]
    if FILE_PATH:
        sheet = pd.read_excel(FILE_PATH, sheet_name=None, index_col=None,
                              dtype={'件号': str, "年度": str, "档案门类": str, "保管期限": str})
        if PDF_PATH:
            start(sheet,PDF_PATH,error,FILE_PATH)
    return error
