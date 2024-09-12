# Python-MySQL-Practice
 Terminal-based user interface where user can search for records in a database through a python script.

 The data's description is also pushed but will be included in this README:


Name dataset
=========================================

The data contains 491,655,925 records from 106 countries. The uncompressed version takes around 10GB on the disk.

Each country is in a separate CSV file. FR is France, DE is Germany... The list of the country codes (ISO alpha2) is provided below.

A CSV file contains rows of this format: first_name,last_name,gender,country_code. Each record is a real person.

Example:
Laure,Canet,F,FR     ----- "Laure" is first name. "Canet" last name. "F" is Female. "FR" is France.
Louis,Givran,M,FR
Timothy,Dovin,M,FR
Anne Marie,Petiton,F,FR
Claudine,Solignac,F,FR

NOTE: Duplicates have not been removed.

Gender
===================================
The gender is either M, F or empty string (missing).

List of country codes
===================================
AE - United Arab Emirates
AF - Afghanistan
AL - Albania
AO - Angola
AR - Argentina
AT - Austria
AZ - Azerbaijan
BD - Bangladesh
BE - Belgium
BF - Burkina Faso
BG - Bulgaria
BH - Bahrain
BI - Burundi
BN - Brunei Darussalam
BO - Bolivia, Plurinational State of
BR - Brazil
BW - Botswana
CA - Canada
CH - Switzerland
CL - Chile
CM - Cameroon
CN - China
CO - Colombia
CR - Costa Rica
CY - Cyprus
CZ - Czechia
DE - Germany
DJ - Djibouti
DK - Denmark
DZ - Algeria
EC - Ecuador
EE - Estonia
EG - Egypt
ES - Spain
ET - Ethiopia
FI - Finland
FJ - Fiji
FR - France
GB - United Kingdom
GE - Georgia
GH - Ghana
GR - Greece
GT - Guatemala
HK - Hong Kong
HN - Honduras
HR - Croatia
HT - Haiti
HU - Hungary
ID - Indonesia
IE - Ireland
IL - Israel
IN - India
IQ - Iraq
IR - Iran, Islamic Republic of
IS - Iceland
IT - Italy
JM - Jamaica
JO - Jordan
JP - Japan
KH - Cambodia
KR - Korea, Republic of
KW - Kuwait
KZ - Kazakhstan
LB - Lebanon
LT - Lithuania
LU - Luxembourg
LY - Libya
MA - Morocco
MD - Moldova, Republic of
MO - Macao
MT - Malta
MU - Mauritius
MV - Maldives
MX - Mexico
MY - Malaysia
NA - Namibia
NG - Nigeria
NL - Netherlands
NO - Norway
OM - Oman
PA - Panama
PE - Peru
PH - Philippines
PL - Poland
PR - Puerto Rico
PS - Palestine, State of
PT - Portugal
QA - Qatar
RS - Serbia
RU - Russian Federation
SA - Saudi Arabia
SD - Sudan
SE - Sweden
SG - Singapore
SI - Slovenia
SV - El Salvador
SY - Syrian Arab Republic
TM - Turkmenistan
TN - Tunisia
TR - Turkey
TW - Taiwan, Province of China
US - United States
UY - Uruguay
YE - Yemen
ZA - South Africa





THOUGHTS AND FEEDBACK
=================================================

The only hard part about this is the connection to Mysql and realising that my importing time for data is already efficient enough for single csv file. (Spent way too long trying to import the whole csv folder in less than 5 minutes.)

Some work around with the logic with validation. 

I think I can improve the construct of the program and make it more compact and neat. 


Note: there will be much more reflection and thoughts after I am done with this program. As of now I am still learning more and more.




UPDATE ONE
=================================================

I am basically done with the back end of the name finder SQL operation. However I still need to write a rigorous testing plan to make sure everything goes according to how I have planned it.

Its is definitely not the neatest code and there is alot of repetition which I will later fix when my program is full functioning (AKA optimisation)
