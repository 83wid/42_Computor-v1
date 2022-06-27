#!/usr/bin/python3

def myAbs(num) :
    return -num if num < 0 else num;

def sqrt(n) :
 
    # Assuming the sqrt of n as n only
    x = n
 
    # To count the number of iterations
    count = 0
 
    while (1) :
        count += 1
 
        # Calculate more closed x
        root = 0.5 * (x + (n / x))
 
        # Check for closeness
        if (myAbs(root - x) < 0.000001) :
            break
 
        # Update root
        x = root
 
    return root
 

import sys
import re

valid = 1;

try :
    inb = str(sys.argv[1]);
    inb = re.sub('\s+',' ',inb).upper();

    if re.compile('^[X0-9\.\^\s\=\*\+\-]+$').match(inb) :
        degree = 0;
        solution = 0;
        power = 0;
        lowPower = 0;
        form = inb;
        # arranging the equation on one side
        equetion = inb.split( "=");
        equetion[0] = equetion[0].strip();
        equetion[1] = equetion[1].strip();
        xposLeft = [i.start() for i in re.finditer("X", equetion[0])];
        xposRight = [i.start() for i in re.finditer("X", equetion[1])];

        eqnSp = re.sub('\s+', '', equetion[1]);
        if eqnSp != "0" :
            equetion[1] = "+ " + equetion[1] if eqnSp[0] != '-' else "- " + equetion[1][1:];
            equetion[1] = equetion[1].replace("^-", '^p');
            equetion[1] = equetion[1].replace("^+", '^j');
            equetion[1] = equetion[1].replace("-", 'k');
            equetion[1] = equetion[1].replace("+", '-');
            equetion[1] = equetion[1].replace("k", '+');
            equetion[1] = equetion[1].replace("^p", '^-');
            equetion[1] = equetion[1].replace("^j", '^+');
            form = "+ " + equetion[0] + " " + equetion[1] + " ";
        else :
            form = "+ " + equetion[0] + " ";

        xpos = [i.start() for i in re.finditer("X\^", form)];
        for i in xpos :
            power = int(form[i + 2:i + 4]);
            if power > degree :
                degree = power;
        i = 0;
        # removing contradicting values without scalars 
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
        
        form =  re.sub('\s+', '', form.replace("X^1", 'X'));

        #protecting  power sign before spliting
        form = form.replace("^-", '^p');
        summ = form.split("-");

        setOfElems = list();
        setofDup = list();
        setSign = list();

        # Calculating elements with scalars and their dups 
        j = 0;
        while j < len(summ):
            elem = summ[j];
            if "+" not in elem:
                if elem in setOfElems:
                    setofDup[setOfElems.index(elem)] += 1 if setSign[setOfElems.index(elem)] == -1 else -1;
                elif elem != "":
                    setOfElems.append(elem)
                    setofDup.append(1);
                    setSign.append(-1);
            elif "-" not in elem:
                sump = elem.split('+');
                el = 0;
                while el < len(sump):
                    elem = sump[el];
                    if elem in setOfElems:
                        setofDup[setOfElems.index(elem)] += 1 if setSign[setOfElems.index(elem)] == 1 else -1;
                    elif elem != "":
                        setOfElems.append(elem)
                        setofDup.append(1);
                        setSign.append(1 if el > 0 else -1);
                    el += 1;
            j += 1;
        finalElem = list();
        finalDup = list();
        finalSign = list();

        # spliting elements from scalars adding scalars to dups.

        j = 0;
        while j < len(setOfElems) :
            elem = setOfElems[j].split("*");
            if len(elem) > 1 and setofDup[j] != 0:
                setofDup[j] = setofDup[j] * float(elem[0]) if setofDup[j] != 1 else float(elem[0]);
                setOfElems[j] = elem[1];
            j += 1;
        i = 0;
        while i < len(setOfElems):
            if "^p" in setOfElems[i]:
                setOfElems[i] = setOfElems[i].replace("^p", "^-");
            elem = setOfElems[i];
            if elem in finalElem:
                finalDup[finalElem.index(elem)] += setofDup[i] * setSign[i];
            else:
                finalElem.append(elem)
                finalDup.append(setofDup[i] * setSign[i]);
            i += 1;
        # creating the new format
        form = "";
        i = 0;
        while i < len(finalElem) :
            if finalDup[i] != 0 :
                form += " " + ("+ " if finalDup[i] > 0  and i != 0 else "") + (str(finalDup[i]) + " * " if finalDup[i] != 1 else "") + finalElem[i];
            i += 1;

        nXElem = 0.0;
        xElems = list();
        xDups = list();
    
        # filtering constant values and adding sum of dup for an elements.
        i = 0;
        while i < len(finalElem) :
            elem = finalElem[i];
            if 'X' not in  elem :
                nXElem += float(elem) * finalDup[finalElem.index(elem)];
            elif elem == "X^0":
                nXElem += finalDup[finalElem.index(elem)];
            else:
                xElems.append(elem);
                xDups.append(finalDup[finalElem.index(elem)]);
            i += 1;

        # creating delta variables.
        a = 0;
        b = 0;
        c = nXElem;
        for elem in xElems :
            if "X^2" in elem :
                a = xDups[xElems.index(elem)];
            elif "X" in elem :
                b = xDups[xElems.index(elem)];

        delta = b * b - 4 * a * c;
        form = "";
        i = 0;
        # creating final reduced form
        while i < len(xElems) :
            if xDups[i] != 0 :
                form += " " + ("+ " if xDups[i] > 0  and i != 0 else "") + (str(xDups[i]) + " * " if xDups[i] != 1 else "") + xElems[i];
            i += 1;
        if nXElem != 0 :
            form += " " + str(nXElem) if nXElem < 0 else " + " + str(nXElem);
    else:
        valid = 0;
except:
    print ("Error");
    exit(0);
finally:

    if valid == 0 :
        print("Error");
        exit(0);
    # calculating the actual degree of the equation
    degree = 1 if 'X' in form else 0;
    form = re.sub('\s+', ' ', form);
    xpos = [i.start() for i in re.finditer("X\^", form)];
    for i in xpos :
        power = int(form[i + 2:i + 4]);
        if power < 0 :
            lowPower = power;
        if power > degree :
            degree = power;

    # print statements
    if lowPower < 0 :
        print ("Reduced form:", form + " = 0");
        print ("Polynomial degree:", "undefined");
        print ("This is not a Polynome, degree is strictly negative");
        exit(0);
    if form == "" :
        print ("Reduced form:", "0 = 0");
        print ("Polynomial degree:", 0);
        print ("The solution is:", "Each real number is a solution.");
        exit(0);

    if  degree < 3 and a == 0 and b == 0 and c != 0 :
        print ("Reduced form:", form + " = 0");
        print ("Polynomial degree:", 0);
        print ("WTF!! I can't solve this using human math.");
        exit(0);

    if degree < 3 and a == 0 :
        print ("Reduced form:", form + " = 0");
        print ("Polynomial degree:", degree);
        print ("The solution is:")
        print("{:.6f}".format(-c / b));
        exit(0);

    print ("Reduced form:", form + " = 0");
    print ("Polynomial degree:", degree);
    if degree > 2 :
        print("The polynomial degree is strictly greater than 2, I can't solve.");
    elif delta < 0:
        print("Discriminant is strictly negative, the two complex solutions are:");
        val = sqrt(-delta/ (2* a));
        print(-b /( 2 * a), " + " if val >= 0 else " - ","{:.6f}".format(abs(val)), " * i");
        print(-b /( 2 * a), " - " if val >= 0 else " + ","{:.6f}".format(abs(val)), " * i");
    elif delta > 0:
        print("Discriminant is strictly positive, the two solutions are:");
        print("{:.6f}".format((-b - sqrt(delta)) /( 2 * a)));
        print("{:.6f}".format((-b + sqrt(delta)) /( 2 * a)));
    elif delta == 0:
        print("Discriminant is Zero, the solution is:");
        print("{:.6f}".format(-b /( 2 * a)));