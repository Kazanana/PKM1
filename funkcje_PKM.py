#
#funkcje_PKM.py
#
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 22:30:09 2022

@author: HP
"""
import sys
sys.path.append(r'C:\Users\HP\my_python_modules')
import normy as normy
# def ladujExcel (Etap1,Etap2,Etap3,Etap4,Etap5,Etap6,Etap7,Etap8,Etap9,Etap10):
    
#     nazwaPliku = r'C:\Users\domin\OneDrive\Desktop\PKM1_2021_Dziurdź\roboczy\B05_Karta wyników PKM_I.xlsx'
#     numerArkusza = 1;
#     zakres = 'F32:J32';
#     struct2ExcelHorizontal(Etap1, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'K32:T32';
#     struct2ExcelHorizontal(Etap2, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'U32:AC32';
#     struct2ExcelHorizontal(Etap3, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'F40:M40';
#     struct2ExcelHorizontal(Etap4, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'N40:Y40';
#     struct2ExcelHorizontal(Etap5, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'Z40:AC40';
#     struct2ExcelHorizontal(Etap6, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'F48:T48';
#     struct2ExcelHorizontal(Etap7, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'G57:S57';
#     struct2ExcelHorizontal(Etap8, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'F66:AB66';
#     struct2ExcelHorizontal(Etap9, nazwaPliku, numerArkusza, zakres);
    
#     zakres = 'F75:X75';
#     struct2ExcelHorizontal(Etap10, nazwaPliku, numerArkusza, zakres);



# def struct2ExcelHorizontal(struct,nazwaPliku,numerArkusza,zakres):

#     etap = struct2cell(struct);
#     writecell(etap,nazwaPliku,'Sheet',numerArkusza,'Range',zakres);
    

def doborWpustu(d):# wyjscie: dobrany wpust
    dobranyWpust={};
    if d <= 22:
        raise ValueError('za mała średnica, d <= 22')
    elif d > 22 and d <= 30:
        dobranyWpust['b'] = 8;
        dobranyWpust['h'] = 7;
        return dobranyWpust;
    elif d > 30 and d <= 38:
        dobranyWpust['b'] = 10;
        dobranyWpust['h'] = 8;
        return dobranyWpust;
    elif d > 38 and d <= 44:
        dobranyWpust['b'] = 12;
        dobranyWpust['h'] = 10;
        return dobranyWpust;
    else:
        raise ValueError('za duża średnica d > 44')

def doborDlugosci(l_c,b):# wyjscie: dobranaDlugosc
    l = [18, 20, 22, 25, 28, 32, 36, 40];
    if b not in [8,10,12]:  
        return "b musi być 8 10 12 \n poźniej dodam inne"
    if b == 8:
        for i in range(len(l)):
            if l[i] >= l_c + b:
                dobranaDlugosc = l[i];
                return dobranaDlugosc;
                break
    elif b == 10:
        for i in range(3,len(l)):
            if l[i] >= l_c + b:
                dobranaDlugosc = l[i];
                return dobranaDlugosc;
                break    
    elif b == 12:
        for i in range(5,len(l)):
            if l[i] >= l_c + b:
                dobranaDlugosc = l[i];
                return dobranaDlugosc;
                break

def doborGwintu(d_r):#[dobranyGwint] wyjscie
    if d_r < 2.9:
        return ValueError('za mała średnica')
    elif d_r >= 100.5:
        return ValueError('za duża średnica')
    
    for i in range(len(normy.gwint)):  
        if normy.gwint[i]['d_3']  < d_r:
            continue
        else:
            dobranyGwint = normy.gwint[i];
            return dobranyGwint

