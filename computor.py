import re
import collections

inb = input();
inb = re.sub('\s+',' ',inb)
degree = 0;
solution = 0;
form = inb;
equetion = inb.split( "=");
# print(equetion)
xposLeft = [i.start() for i in re.finditer("X", equetion[0])];
xposRight = [i.start() for i in re.finditer("X", equetion[1])];
equetion[1] = "+" + equetion[1] if equetion[1][0] != '-' or  equetion[1][0] != '+' else  equetion[1];
equetion[1] = equetion[1].replace("-", 'k');
equetion[1] = equetion[1].replace("+", '-');
equetion[1] = equetion[1].replace("k", '+');

form = equetion[0] + " " + equetion[1] + " ";

xpos = [i.start() for i in re.finditer("X\^", form)];
for i in xpos :
    power = int(form[i + 2]);
    if power > degree :
        degree = power;
i = 0;    
while i <= power :
    var = "X^" + str(i)
    if "- " + var in form :
        if "+ " + var in form :
           form = form.replace("- " + var, ''); 
           form = form.replace("+ " + var, '');
    i += 1;
if "- X " in form :
    if "+ X " in form :
        form = form.replace("- X", ''); 
        form = form.replace("+ X", ''); 

form = re.sub('\s+', ' ', form);
form =  form.replace("X^1", 'X'); 
summ = form.split('-');

setOfElems = list();
setofDup = list();
setSign = list();
for elem in summ:
    if "+" not in elem:
        if elem in setOfElems:
            setofDup[setOfElems.index(elem)] += 1;
        else:
            setOfElems.append(elem)
            setofDup.append(1);
            setSign.append(-1);
    elif "-" not in elem:
        sump = elem.split('+');
        for elem in sump:
            if elem in setOfElems:
                setofDup[setOfElems.index(elem)] += 1;
            else:
                setOfElems.append(elem)
                setofDup.append(1);
                setSign.append(1);

finalElem = list();
finalDup = list();
finalSign = list();


for i in setOfElems :
    elem = i.split("*");
    if len(elem) > 1 :
        setofDup[setOfElems.index(i)]  = setofDup[setOfElems.index(i)] + int(elem[0]) if setofDup[setOfElems.index(i)] > 1 else int(elem[0]);
        setOfElems[setOfElems.index(i)] = elem[1];

i = 0;
while i < len(setOfElems):
    elem = setOfElems[i];
    if elem in finalElem:
        finalDup[finalElem.index(elem)] += setofDup[i] * setSign[i];
    else:
        finalElem.append(elem)
        finalDup.append(setofDup[i] * setSign[i]);
    i += 1;

form = "";
i = 0;
while i < len(finalElem) :
    form += " " + ("+ " if finalDup[i] > 0  and i != 0 else "") + (str(finalDup[i]) + " *" if finalDup[i] > 1 else "") + finalElem[i];
    i += 1;


degree = 0
form = re.sub('\s+', ' ', form);
xpos = [i.start() for i in re.finditer("X", form)];
for i in xpos :
    if form[i + 1] != "^" :
        power = 1;
    else:
        power = int(form[i + 2])
    if power > degree :
        degree = power;
print ("Reduced form:", form);
print ("Polynomial degree:", degree);
print ("The solution is:",  solution if 0 <= degree < 3 else "The polynomial degree is strictly greater than 2, I can't solve.");