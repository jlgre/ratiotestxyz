#!/usr/bin/python3
#import math
import sympy
from sympy import sympify
from sympy import *
#import sys
#from flask_cors import CORS
#
#from flask import Flask, request, jsonify
#
#app = Flask(__name__)
#CORS(app)

#n= symbols('n', integer=True)
n= symbols('n')


# list of accpectable characters
ops=['+','-','*','/','(',')']#,'^','!'] # let's start with these and later we can add e,pi,sin,cos,log
nums=['1','2','3','4','5','6','7','8','9','0','.']
var='n'
#par=['(',')']
words=[' ','factorial','sin','cos','exp','ln','pi']# we can change these to be consistent with sympy

def filter(summand):
    '''
        checks that there are only acceptable characters
        returns indices of first unnacceptable word or
        returns True if they're all good
    '''
    sx = summand
    if 'x' in sx:
        return 'x'
    else:
        '''
        changes all the acceptable characters to 'x'
	the order is important. Like if you changed the n's first, 
	then sin would be si which is not acceptable
        '''
        for s in words:
            if s in sx:
                sx=sx.replace(s,'x'*len(s))
        for s in ops:
            if s in sx:
                sx=sx.replace(s,'x'*len(s))
        for s in nums:
            if s in sx:
                sx=sx.replace(s,'x'*len(s))
        for s in var:
            if s in sx:
                sx=sx.replace(s,'x'*len(s))
        # if any characters have not been changed, they are not acceptable
        for i in range(0,len(sx)):
                if sx[i] != 'x':
                    j=i
                    while sx[j] != 'x':
                        j=j+1
                    return [i,j]
        return True




def ratio():
    '''
    first entry
        0         - it calculated a limit, limit is the second entry
        1         - math typo
        2         - unnacceptable input
    '''
    seq=input('Enter summand: ')
    f=filter(seq)
    if f is True:
        try:
            # converts the string seq into a sympy object (or something)
            # this doesn't work if its a nonsensical math statement like n+*5
            seq=sympify(seq)
        except SympifyError as inst:
            errorMessage = [type(inst),inst.args]
            return [1,errorMessage]
        else:
            # computes the ratio and limit
            res=limit(seq/seq.subs(n,n-1),n,oo)
            if res == 1:
                return [0,1]
            elif res > 1:
                return [0,res]
            else:
                return[0,res]
    else:
        errorMessage = seq+'\n' + ' '*f[0]+'^'*(f[1]-f[0]) # underlines first unnaceptable phrase
        return [2,errorMessage]


#@app.route('/ratioTest', methods = ['POST', 'GET'])
#def run():
#        print(request.args['summand'], file=sys.stdout)
#        global ss
#        ss = get(request.args['summand'])
#        print(ss, file=sys.stdout)
#        res = ratio()
#        message = ''
#
#        if res[0] == 0:
#                message = "Test inconclusive"
#        elif res[0] == -1:
#                message = "Series probably converges"
#        elif res[0] == 1:
#                message = "Series probably diverges"
#        return jsonify(result = message,
#                       num = float(res[1])
#        )
#
#
#if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=8000)
#