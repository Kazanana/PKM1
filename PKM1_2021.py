#Oh shit, here we go again
import sys
import math as m
import sympy as sp
import pandas as pd
import funkcje_PKM as PKM
sys.path.append(r'C:\Users\HP\Desktop\PKM1')
# %% ETAP I
Q = 15.5e03;
W = 235;
# rodzajKorpusu = 'KO';


#stal St5
R_h = 265;
R_e = 295;
x_w = 7;
P_kr = x_w*Q;
E = 2.1e05;
lambda_gr = m.pi*m.sqrt(E/R_h);


l = W + 80;
l_w = 2 * l;

A = R_e;
B = ((R_h-R_e)*4*l_w)/lambda_gr;
C = -(P_kr*4)/m.pi;
delta  =  B**2  -  4*A*C;              
if  delta  > 0:
    d1 = ( - B - m.sqrt(delta))/(2*A);  d2 = (-B + m.sqrt(delta))/(2*A);
elif delta == 0:
    d1 =- B/(2*A);  d2 = d1;
else:
    d1=None;  d2=None;                      

if d1>0:
    d_min=d1
elif d2>0:
    d_min=d2;
else:
    print('coś zjebałeś')


lambda_= 4 * l_w/d_min;

if lambda_< lambda_gr:
    wzor = 'T-J';
    #print(['Spełnione warunki dla wzoru ', wzor])
elif lambda_> lambda_gr:
    wzor = 'E';
    #print(['Spełnione warunki dla wzoru ', wzor])
    d_min = ( (64*x_w*Q*l_w**2)/(m.pi**3*E) )**(1/4);
else:
    print('lambda=lambda_gr')

lambda_= 4 * l_w/d_min;
etap1 = {}

etap1['l_w'] = l_w;
etap1['d_min'] = d_min;
etap1['wzor'] = wzor;
etap1['lambda_']= lambda_;
etap1['lambda_gr'] = lambda_gr;
sruba = PKM.doborGwintu(d_min);

# clear delta d1 d2  A B C wzor d_min

# %% ETAP II
mu_min = 0.08;
gamma = m.degrees(m.atan( sruba['P']/(m.pi*sruba['d_2']) ));
rho_prime_min = m.degrees (m.atan( mu_min/m.cos(m.radians(15)) ) );

etap2 = {}
etap2['gwint'] = f'Tr{sruba["d"]}x{sruba["P"]}';
etap2['d'] = sruba['d'];
etap2['P'] = sruba['P'];
etap2['d_2'] = sruba['d_2'];
etap2['d_3'] = sruba['d_3'];
etap2['D_1'] = sruba['D_1'];
etap2['D_4'] = sruba['D_4'];
etap2['mu_min'] = mu_min;
etap2['rho_prime_min'] = rho_prime_min;
etap2['gamma'] =gamma;


# %% Etap III
d_r = sruba['d_3'];
d_s = sruba['d_2'];
mu_max = 0.12;
rho_prime_max = m.degrees( m.atan( mu_max/m.cos(m.radians(15)) ) );
F = Q * m.tan( m.radians(gamma + rho_prime_max) );

lambda_rz = 4*l_w/d_r;
sigma_kr = m.pi**2*E/(lambda_rz**2);
sigma_c = (4*Q)/(m.pi*d_r**2);
#M_s = 0.5*d_s*Q*tand(gamma+rho_prime_max);
M_s = 0.5*F*d_s;
tau_s = (16*M_s)/(m.pi*d_r**3);
sig_z = m.sqrt(sigma_c**2+3*tau_s**2);
X_rz = sigma_kr/sig_z;

etap3 ={}
etap3['lambda_rz'] = lambda_rz;
etap3['sigma_kr'] = sigma_kr;
etap3['mi_max'] = mu_max;
etap3['rho_prime_max'] = rho_prime_max;
etap3['M_s'] = M_s*10**-3;
etap3['sigma_c'] = sigma_c;
etap3['tau_s'] = tau_s;
etap3['sig_z']= sig_z;
etap3['X_rz'] = X_rz;



# %% Etap IV
#materiał nakrętki
#Brąz BA1032
R_m_braz = 600;
E_n = 1.15*10**5;
nu_braz = 0.32;
#materiał korpusu
#żeliwo EN-GJL-300
#
#
#    TUTAJ INACZEJ DLA STALOWEGO
#
#
R_m_zeliwo = 300;
E_k = 1.08*10**5;
nu_zeliwo = 0.26;

X_q = 3.5;

Q_c_zeliwo = 1.8*R_m_zeliwo;
Q_c_braz = 0.6*R_m_braz;
k_c_braz = Q_c_braz/X_q;
k_c_zeliwo = Q_c_zeliwo/X_q;

p_r_zeliwo = 0.15*k_c_zeliwo;
p_r_braz = 0.15*k_c_braz;

p_s_zeliwo = 0.8*k_c_zeliwo;
p_s_braz = 0.8*k_c_braz;

if p_r_braz > p_r_zeliwo:
    #print('dla żeliwa mniejsze');
    p_r = p_r_zeliwo;
else:
    #print('dla brązu mniejsze')
    p_r = p_r_braz;

p_r = round(p_r);

if p_s_braz>p_s_zeliwo:
    #print('dla żeliwa mniejsze');
    p_s = p_s_zeliwo;
    
else:
    #print('dla brązu mniejsze')
    p_s = p_s_braz;

p_s = round(p_s - p_s % 10);

A_c = Q/p_r;
d = sruba['d'];
D_1 = sruba['D_1'];
A_1 = (m.pi/4) * (d**2-D_1**2);
z = A_c/A_1;
z_c = z + 1.5;

P = sruba['P'];
w = 1.5*P;
W_g = m.ceil(w);#zaokrąglanie w górę

h = z_c*P + W_g;
H_n = m.ceil(h);

E_s = E;#moduł young'a dla śruby
d_3 = sruba['d_3'];
D_4 = sruba['D_4'];
D_N_1 = m.sqrt( (E_s/E_n)*d_3**2 + D_4**2 );
D_N_1_excel = D_N_1;
D_N_1 = round(D_N_1);

D_N_2 = m.sqrt(4*Q/(m.pi*p_s) + (d+2)**2) + 2;
D_N_2_excel = D_N_2;
D_N_2 = m.ceil(D_N_2);

if D_N_2 > D_N_1:
    D_N = D_N_2;
else:
    D_N = D_N_1;

etap4 = {}
etap4['p_r'] = p_r;
etap4['z_c'] = z_c;
etap4['W_g'] = W_g;
etap4['H_n'] = H_n;
etap4['D_N_1'] = D_N_1_excel;
etap4['p_s'] = p_s;
etap4['D_N_2'] = D_N_2_excel;
etap4['D_N'] = D_N;



# clear A_c A_1 D_N_1 D_N_2 naciskiRuchowe naciskiStatyczne + ...
#     w W_g h z z_c

# %%Etap Va
#
#    TUTAJ INACZEJ DLA STALOWEGO
#   
# 
# 
# (dla korpusu spawanego będzie + 30)
D_K = D_N + 40;
mu_w = 0.08;
X_w = 1.5;
#odejmuję 4mm (można 5)
H_w = H_n - 4;
p_min = (2*X_w*M_s)/(mu_w*m.pi*D_N**2*H_w);
#1-nakrętka,brąz 2-korpus,żeliwo
nu_1 = nu_braz;
nu_2 = nu_zeliwo;
alpha_1 = D_4/D_N;
alpha_2 = D_N/D_K;
C_1 = ((1+alpha_1**2)/(1-alpha_1**2)) - nu_1;
C_2 = ((1+alpha_2**2)/(1-alpha_2**2)) + nu_2;
#założenie d = D_N
E_1 = E_n;
E_2 = E_k;
delta = D_N*p_min*(C_1/E_1 + C_2/E_2);
etap5 = {}
etap5['D_K'] = D_K;
etap5['mu_w'] = mu_w;
etap5['X_w'] = X_w;
etap5['p_min'] = p_min;
etap5['delta_1'] = delta*10**3;
# %% Etap Vb
#stopnień odkształceń plastycznych wierzchołków nierówności
# powierzchni podczas montażu a= 0.4 - 0.6
# ZMIENIĆ 
a = 0.6;
h_1 = 4;#[um]
h_2 = 4;
delta_m = delta*10**3 + 2*a*(h_1 + h_2);#[um]
# delta_m = round(delta_m);
#
#
#   TUTAJ TOLERANCJE TRZEBA DOBRAĆ NA PODSTAWIE delta_m
#   prezentacja Vb 8-9 stron
#
IT7 = 30;#um
delta_m_max = 72;#[um]es wartości dla tolerancji wałka s6 D_N=51[mm]
delta_m_min = 53 - IT7;#[um]ei

etap5['h_1'] = h_1;
etap5['h_2'] = h_2;
etap5['delta_2'] = etap5['delta_1'];
etap5['delta_m'] = delta_m;
etap5['PAS'] = 'H7/s6';
etap5['delta_m_min'] = delta_m_min;
etap5['delta_m_max'] = delta_m_max;

# %%Etap VI
delta_max = delta_m_max - 2*a*(h_1 + h_2);#[um]
p_max = (delta_max*10**-3/D_N)*( 1/(C_1/E_1 + C_2/E_2) );#[MPa]
#zmienna pomocnicza 
u = (1+alpha_2**2)/(1-alpha_2**2);

sigma_1_red = p_max*( 2/(1 - alpha_1**2) );
sigma_2_red = p_max*m.sqrt(1+u+u**2);
etap6 = {}
etap6['delta_max'] = delta_max;
etap6['p_max'] = p_max;
etap6['sigma_1_red'] = sigma_1_red;
etap6['sigma_2_red'] = sigma_2_red;


# %%Etap VII
phi_z = D_N - 2;
x_q = 6;
k_t_korpus = (0.6 * R_m_zeliwo)/x_q;
g_kk = Q/(m.pi * phi_z * k_t_korpus);#policzona
g_kk_p = m.ceil((g_kk+2));#przyjęta

d_w = d_3;
k_t_sruba = (0.62*R_e)/x_q;
k_t_sruba = m.floor(k_t_sruba);
R_e_pierscien = 235;
k_t_pierscien = (0.62*R_e_pierscien)/x_q;
k_t_pierscien = round(k_t_pierscien);

g_ks = Q/(m.pi*d_w*k_t_sruba);#policzona
g_ks_p = m.ceil((g_ks+2));#przyjęta


d_ks = m.sqrt(((4*Q)/(m.pi*p_s))+D_4**2);
d_ks = m.ceil(d_ks);#przyjęta


#D<d3, stal S235
# wymiar wałka na m.pierścień osadczy (z)
# 
#
#     TUTAJ DLA WIĘKSZYCH ŚRUB BĘDZIE WIĘKSZY WAŁEK
#
#
D = 24;
D_1_czop = 22.9;
f_czop = 1.3;
h_czop = 4;
D_0 = 22.2;
b_pierscien = 3;
F_w = 1010 * 9.80665; 
d_t = 2*(D_0/2 + b_pierscien);
# m.pierścień oporowy z takiego samego materiału co śruba
g_p = F_w/(m.pi*d_t*k_t_pierscien);
g_p = m.ceil(g_p);
etap7 = {}
etap7['phi_z'] = phi_z;
etap7['k_t_korpus'] = k_t_korpus;
etap7['g_kk'] = g_kk;
etap7['g_kk_p'] = g_kk_p;
etap7['d_w'] = d_w;
etap7['k_t_sruba'] = k_t_sruba;
etap7['g_ks'] = g_ks;
etap7['g_ks_p'] = g_ks_p;
etap7['p_s'] = p_s;
etap7['d_ks'] = d_ks;
etap7['D'] = D;
etap7['F_w'] = F_w;
etap7['d_t'] = d_t;
etap7['k_t_m.pierscien'] = k_t_pierscien;
etap7['g_p'] = g_p;


# %% Etap VIII
T = 250e-03;
nu_1 = 0.3;
nu_2 = 0.32;
E_1 = 2.1e05;
E_2 = 1.15e05;
psi = (1 - nu_1**2)/E_1 + (1 - nu_2**2)/E_2;
sigma_dH = 500;

r_s = sp.Symbol('r_s', positive=True)
eq = 1/m.pi * ( (6* (2*T/(psi*r_s**2))**2 * Q) )**(1/3) - sigma_dH;
r_s = sp.solve(eq);
r_s_rz = round(r_s[0]*3);# większy trzeba przyjąć żeby gamma było odpowiednie


d_OG = 6;
mu = 0.12;
M_k = Q * d_OG/2 * mu;
M_c = M_s + M_k;
d_czop = d_w;
F_o = 2 * M_c/d_czop;


wpust = PKM.doborWpustu(d_czop);

#materiał wpustu C45
#materiał koła zapadkowego S235
#najsłabszy, więc liczę p_s dla niego
x_q = 2.3;
R_e_kolo = 235;
Q_c_kolo = R_e_kolo;
k_c_kolo = Q_c_kolo/x_q;
p_s_kolo = round(0.8*k_c_kolo,-1);


l_c = 4*M_c/(d_czop * p_s_kolo * wpust['h']);
l_cal_wpust_norma = PKM.doborDlugosci(l_c, wpust['b']);

etap8 = {}
etap8['sigma_dH'] = sigma_dH;
etap8['r_s']= r_s;
etap8['T'] = T*10**3;
etap8['d_OG'] = d_OG;
etap8['M_k'] = M_k*10**-3;
etap8['M_c'] = M_c*10**-3;
etap8['d'] = d_czop;
etap8['F_o'] = F_o;
etap8['b'] = wpust['b'];
etap8['h'] = wpust['h'];
etap8['p_s'] = p_s;
etap8['l_c'] = l_c;
etap8['l'] = l_cal_wpust_norma;


# %%
#Etap IX
#wymiary koła
h_M = l_cal_wpust_norma + 4;
g_b = 4;
h_p = h_M - 2*g_b;
h_k = h_p - 2;
d_z = 2*d_czop;
a_kolo = d_z - 10;
#wstępne
r_F_wstepne = (d_z + a_kolo)/4;
#szerokosc rowka
b_kolo = 10;


#sworzen 8
d_sworznia = 8;
g_pp = 2;
y = g_pp + h_M;
d_0 = 2;
w = 3;
l_sworzen = y + d_0/2 + w;
b_z = h_M - 2*(g_b + g_pp);


c = 2*m.sqrt(d_z**2/4 - b_kolo**2/4);
#długość boku rowka
X = c/2 - a_kolo/2;

r_F = m.sqrt( (a_kolo + X)**2/4 + b_kolo**2/4 );
F_o = M_c/r_F;


beta = m.atan( b_kolo/(a_kolo + X) );# w radianach
F_N = F_o*m.cos(beta);
A_p = b_z*X;
sigma_p = F_N/A_p;
p_s_kolo;
if sigma_p > p_s_kolo:
    raise ValueError('sigma_p > p_s_kolo');


# TUTAJ TRZEBA ZAPROJEKTOWAĆ ZAPADKĘ
#
#   Ja zrobiłem tak:
#   - ustaliłem na początku alpha i a_o takie, żeby theta wyszło w zakresie
#   od 5 do 10
#   - dla ustalonych a_o i aplpha narysowałem zapadkę 
#
#   Zapadkę rysowałem tak, że najm.pierw dobrałem środek promieni i potem
#   dobierałem ich długości żeby wmiarę w porządku wyglądała zapadka we
#   współpracy z kołem
#
a_o = d_z/2 + 4 + 17;

alpha = m.radians(50);
c_F = r_F/m.cos(alpha);
b = r_F*m.tan(alpha);
c = a_o - c_F;

a = m.sqrt( b**2 + c**2 - 2*b*c*m.cos( m.radians(90) + alpha ) );
theta = m.asin( c/a * m.sin(m.radians(90) + alpha) );
R = F_o/m.cos(theta);
#klasa wytrzymałości sworznia 5.6
R_m_sworznia = 500;
R_e_sworznia = 0.6 * R_m_sworznia;
Q_g_sworznia = 1.19 *R_e_sworznia;
x_q = 2.3;
k_g_sworznia = Q_g_sworznia/x_q;
W_x = m.pi*d_sworznia**3/32;
M_g_max = R/2 * (1/2 * g_b + g_pp + 1/4 * b_z);
sigma_g_sworznia = M_g_max/W_x;
if sigma_g_sworznia > k_g_sworznia:
    raise ValueError('sigma_g > k_g_sworznia');

#
#
#        TUTAJ TRZEBA ZMIERZYĆ TE SZEROKOŚCI
#   przekrój zapadki w odległości 4mm od 
#   przyłożenia siły reakcji R
#
#
#
h_4 = 8.6;
f_4 = 2.29;
A_p_4 = b_z * h_4;
W_x_4 = b_z*h_4**2/6;
sigma_c_4 = R/A_p_4;
sigma_g_4 = R*f_4/W_x_4;
sigma_z_4 = sigma_c_4 + sigma_g_4;
R_e_zapadka = R_e_kolo;
Q_g_zapadka = 1.19 * R_e_zapadka;
k_g_zapadka = round(Q_g_zapadka/x_q,-1);

if sigma_z_4 > k_g_zapadka:
   raise ValueError('sigma_z_4 > k_g_zapadka');


#kolo na rozciąganie 
# tego nie było w prezentacji ale chciałem się upewnić
# jakby sigma_r_kolo > k_r_kolo to trzeba by koło zapadkowe i
# zapadkę od nowa większe
rowek_piasta = 3.3;
A_kolo_r = h_k * (a_kolo/2 - d_czop/2 - rowek_piasta);
sigma_r_kolo = F_o/A_kolo_r;
k_r_kolo = R_e_kolo/x_q;
if sigma_r_kolo > k_r_kolo:
    raise ValueError('sigma_r_kolo > k_r_kolo');

etap9 = {}
etap9['h_M'] = h_M;
etap9['g_b'] = g_b;
etap9['h_k'] = h_k;
etap9['d_z'] = d_z;
etap9['a'] = a_kolo;
etap9['r_F'] = r_F_wstepne;
etap9['n'] = 6;
etap9['b_z'] = b_z;
etap9['a_sworznia'] = d_sworznia;
etap9['l'] = l_sworzen;
etap9['b'] = b_kolo;
etap9['X'] = X;
etap9['r_F_rzecz'] = r_F;
etap9['F_o'] = F_o;
etap9['F_N'] = F_N;
etap9['sigma_p'] = sigma_p;
etap9['p_s'] = p_s_kolo;
etap9['R'] = R;
etap9['sigma_g'] = sigma_g_sworznia;
etap9['XY'] = '5.6';
etap9['k_g_sworznia'] = k_g_sworznia;
etap9['sigma_z'] = sigma_z_4;
etap9['k_g_zapadka'] = k_g_zapadka;


# %%Etap X
# Tutaj patrzyłem jak wygląda to u niego na prezentacji i mi wyszły takie
# wymiary z grubsza
#
#
#
szerokosc_obudowa = d_z + 2;
a_kwadrat = szerokosc_obudowa - 20;
w = 80 - a_kwadrat/2 - 3; #to 80 wynika z rysunku na prezentacji tak na oko
r = a_kwadrat*m.sqrt(2)/2;

F_R = 250;
r_R = M_c/F_R;
r_M = r_R - w;

F_1 = F_R/4;
M_F = F_R*r_M;
F_2 = M_F/(4 * r);
alpha = m.radians(45);

F_W = m.sqrt(F_1**2 + F_2**2 + 2*F_1*F_2*m.cos(alpha));
mu_srubaM = 0.08;
F_r = F_W/(2 * mu_srubaM);

#wstępnie przyjmuję M8 5.6
#taką kazał przyjąć
d_3_M = 6.355;

A_p = m.pi/4 * d_3_M**2;
sigma_r_srubaM = F_r/A_p;
sigma_z_srubaM = 1.17*sigma_r_srubaM;

R_e_srubaM = 300;
Q_r_srubaM = R_e_srubaM;
k_r_srubaM = m.ceil(Q_r_srubaM/x_q);

if sigma_z_srubaM > k_r_srubaM:
    raise ValueError('sigma_z_srubaM > k_r_srubaM');


#rura bezszwowa z normy DIN 2448
# z norm w necie
# jak za cienką ściankę weźmiesz to nie spełni warunku na zginanie
D_rura = 13.5;
grubosc_scian = 3.2;
d_rura = D_rura - 2 * grubosc_scian;

W_x_rura = m.pi*(D_rura**3 - d_rura**3)/32;
l_rura = r_M - 50;

sigma_g_rura = F_R*l_rura/W_x_rura;
R_e_rura = 235;
Q_g_rura = R_e_rura;
k_g_rura = R_e_rura * 1.19/x_q;

if sigma_g_rura > k_g_rura:
    raise ValueError('sigma_g_rura > k_g_rura');

A_rz = g_b * 8;
sigma_d = F_r/(2 * A_rz);
k_d = 190;
if sigma_d > k_d:
    raise ValueError('sigma_d > k_d');

etap10 = {}
etap10['F_R'] = F_R;
etap10['r_R'] = r_R;
etap10['r_M'] = r_M;
etap10['M_F'] = M_F*10**-3;
etap10['F_1'] = F_1;
etap10['F_2'] = F_2;
etap10['alpha'] = m.degrees(alpha);
etap10['F_W'] = F_W;
etap10['mu'] = mu_srubaM;
etap10['T'] = F_W/2;
etap10['gwint'] = 'M8x1.25';
etap10['sigma_z_srubaM'] = sigma_z_srubaM;
etap10['XY'] = '5.6';
etap10['k_r_srubaM'] = k_r_srubaM;
etap10['D_rura'] = D_rura;
etap10['d_rura'] = d_rura;
etap10['sigma_g_rura'] = sigma_g_rura;
etap10['k_g_rura'] = k_g_rura;
etap10['sigma_d'] = sigma_d;




# %%Etap XI
p_dop = 3;

#wymiary korpusu
# na prezentacji takie pochylenie było dla żeliwnego
X_pochylenie = 10;
g_s_korpus = 8;#grubosc sciany

# TUTAJ TRZEBA DOBRAĆ
# zabezm.pieczenie sruby
# h_sruby jest podane w normie w prezentacji przy liczeniu zapbezm.pieczeń
# minimalne jest podane ja przyjąłem trochę większe
f_rowek_sruba = 1.3;
h_sruba = 3;
odstep_blacha = 3;#odstęp końca śruby od blachy

l_korpus = round(W + g_p + f_rowek_sruba + h_sruba + odstep_blacha);
d_1_korpus = D_K - 2 * g_s_korpus;
d_k = round(d_1_korpus + l_korpus/X_pochylenie);

# 20 mm z każdej strony na blachę
zabezp_blachy = 20;
d_otwor = d_k + 2 * zabezp_blachy;

D_p = sp.Symbol('D_p', positive=True)

eq = Q/( m.pi/4 * (D_p**2 - d_otwor**2) ) - p_dop
D_p = sp.solve(eq);
D_p = m.ceil(D_p[0]);

f = (D_p - d_k)/2;
M_g_korpus = Q/2 * f;
Q_g_korpus = 1.2*R_m_zeliwo;
k_g_korpus = Q_g_korpus/3.5;
k_g_korpus = k_g_korpus - k_g_korpus%5;
h_p_korpus = sp.Symbol('h_p_korpus', positive=True)

b = m.sqrt(D_p**2 - d_k**2);
W_x_korpus = b*h_p_korpus**2/6;
eq = M_g_korpus/( b*h_p_korpus**2/6 ) - k_g_korpus
h_p_korpus = sp.solve(eq);
h_p_korpus = m.ceil(h_p_korpus[0]);

spr = Q*6/(M_c*2*m.pi)
# %%

nazwy = [f'Etap{i}' for i in range(1,11) ]
etapy = [etap1, etap2, etap3, etap4, etap5, etap6, etap7, etap8, etap9, etap10]
sciezka=r'C:\Users\HP\Desktop\PKM1\B00_Karta Wyników PKM_I.xlsx'
PKM.ladujexcel(etapy,nazwy, sciezka)
# %% Wyswietl etapy
# for i in range(len(etapy)):
    # print(f'{nazwy[i]} :\n{etapy[i]}')