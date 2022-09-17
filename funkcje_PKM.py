#
#funkcje_PKM.py
#
# -*- coding: utf-8 -*-

import sys
import pandas as pd
import normy as normy
sys.path.append(r'C:\Users\HP\my_python_modules')
def ladujexcel(etapy, nazwy, path):
    if type(etapy) != list or type(nazwy) != list :
        raise TypeError('Oba argumenty muszą być listami')
    if len(etapy) != len(nazwy):
        raise ValueError('Oba argumenty muszą być tych samych długości')
    dataframes = []
    for i in range(len(etapy)):
        dataframes.append(pd.DataFrame.from_dict(etapy[i], orient='index', columns=[nazwy[i]]))
    for i in range(len(dataframes)):
        with pd.ExcelWriter(path,engine="openpyxl",mode='a',if_sheet_exists='replace') as writer:
            dataframes[i].to_excel(writer, sheet_name=nazwy[i])

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

