#!/usr/bin/python3
import math
import decimal
import random
import sys
from flask_cors import CORS

from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

# global variables
ss = ''
tol = 0.001
cap=10
capu=20
capd=50
capl=20
larger=10000
largei=100

# list of accpectable characters
ops=['+','-','*','/','^','!'] # let's start with these and later we can add e,pi,sin,cos,log
nums=['1','2','3','4','5','6','7','8','9','0','.']
var='n'
par=['(',')']
# gets the input and converts it into a string which can be 'eval'-ed
def get(summand):
        an='' # formula string
        s = summand + 'x'
        i=-1
#       for i in range(0,len(s)):
        while (i < (len(s)-1)):
                i=i+1
                if s[i] in ops:
                        # do whatever with each symbol
                        if s[i]==ops[0]:
                                an=an+'+'
                        if s[i]==ops[1]:
                                an=an+'-'
                        if s[i]==ops[2]:
                                an=an+'*'
                        if s[i]==ops[3]:
                                an=an+'/'
                        if s[i]==ops[4]:
                                an=an+'**'
                        if s[i]==ops[5]:
                                if an[-1] == ')': # need to modify to handle multiple parentheses
                                        j=0
                                        while an[len(an)-(1+j)] != '(':
                                                j=j+1
                                        an=an[0:len(an)-(1+j)]+'(math.factorial('+an[len(an)-j:len(an)]+')'
                                else: #this will only happen if they do something like 5!. n! is actually fine
                                        print('please enter '+s[i-1]+'! as ('+s[i-1]+')!') 
                                        return 1
                elif (s[i] in var):
#                       an+='decimal.Decimal('+s[i]+')'
                        if s[i+1] == ops[5]:
#                               an+='decimal.Decimal(math.factorial(n))'
                                an+='math.factorial(n)'
                                i=i+1 # skips reading the !
                        else:
                                an+=s[i]
                elif s[i] =='(':
#                       j=0
#                       while s[i+j] != ')':
#                               j=j+1
                        an+='decimal.Decimal'+s[i]
                elif s[i] in nums:
                        j=0
                        while (s[i+j] in nums): #counts the number of digits
                                j=j+1
                        an+='decimal.Decimal('+s[i:i+j]+')'
                        i=i+j-1
                elif s[i] ==')':
                        an+=')'
                elif s[i]=='x':
                        print(an, file=sys.stdout)
                        return an
                else: # if the input contains a bad character, it ends the program and prints the first bad character
                        print(s[i],' is not an acceptable character', file=sys.stdout)
                        return 0


def a(n):
        global ss
# this is where the input string puts the input
# here are a few test sequences
        return eval(ss)
#       an=1.0/n # this one is inconclusive, the ratio converges to 1, but program works
#       an=decimal.Decimal(math.factorial(n))/decimal.Decimal((5  ** n)) # this one diverges (now it works)
#       an=decimal.Decimal(math.factorial(n))/decimal.Decimal((n ** n)) # this one converges (now it works but gets real slow around 15,000)
#       an=decimal.Decimal(n ** 2+3 ** n)/(decimal.Decimal(7 ** n)) # this ratio converges to 3/7 (now it works but gets real slow around n=10,000)
        return an

def ratio():
        diff=10
        i=0
        t=0
        s=0
        r=0
        q=0
        n=50 # start at 50 so things like log are not a problem. eventually it should start at the largest number in the formula
        #a0=a(decimal.Decimal(n))/a(decimal.Decimal(n-1))
        a0 = a(n)/a(n-1)
        prev=a0
        cur=0
        while (t< cap) & (s < capd) & (r < capu) &(q < capl):
                n=n+random.randint(1,n) #This way the numbers get large fast but they don't have a pattern
                i=i+1 # just counting the number of iterations
                #cur=a(decimal.Decimal(n))/a(decimal.Decimal(n-1)) # the infamous "ratio"
                cur = a(n)/a(n-1)
                print(n,cur)
                diff=cur-prev
                # there are 4 ways for the algorithm to stop.
                # First, if 'diff' is smaller than 'tol' for 'cap' consecutive iterations
                if abs(diff)<tol :
                        t=t+1
                else:
                        t=0
                # Second, if the ratio 'cur' is smaller than 1 and decreasing 'capd' consecutive times
                if (diff <0) & (cur <1) :
                        s=s+1
                else: 
                        s=0
                # Third, if the ratio 'cur' is larger than 1 and increasing 'capu' consecutive times
                if (diff >0) & (cur >1) :
                        r=r+1
                else:
                        r=0
                # Fourth, if the ratio is too large for large indices
                if (cur > larger) & (n > largei):
                        u=u+1
                else:
                        u=0 
                prev=cur
        print('Ratio =',prev,i,'iterations',n,'th term')

        if abs(prev-1) < tol:
                p=0
                print('Test inconclusive')
        elif prev <1:
                p=-1
                print('Series probably converges')
        else:
                p=1
                print('Series probably diverges')
        return [p,prev]

@app.route('/ratioTest', methods = ['POST', 'GET'])
def run():
        print(request.args['summand'], file=sys.stdout)
        global ss
        ss = get(request.args['summand'])
        print(ss, file=sys.stdout)
        res = ratio()
        message = ''

        if res[0] == 0:
                message = "Inconclusive"
        elif res[0] == -1:
                message = "Converges"
        elif res[0] == 1:
                message = "Diverges"
        return jsonify(result = message,
                       num = float(res[1])
        )


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8000)
