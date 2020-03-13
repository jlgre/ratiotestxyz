#!/usr/bin/python3
import sympy
from sympy import sympify
from sympy import *
import sys
from flask_cors import CORS

from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

n= symbols('n')


# list of accpectable characters
ops=['+','-','*','/','(',')']#,'^','!'] # let's start with these also, ** is exponentiation
nums=['1','2','3','4','5','6','7','8','9','0','.']
var='n'
words=['factorial','sin','cos','exp','ln']# 

def filter(summand):
    '''
    Checks that there are only acceptable characters
    Parameters:
        summand (string): The summand to check
    Returns:
        err (string): The first unnacceptable character found
        True: if all acceptable characters
    '''
    sx = summand+' '
    # changes all the acceptable characters to ' '
    # the order is important. Like if you deleted the 'n's first, 
    # then 'sin' would be 'si ' which is not acceptable.
    # also, if you just deleted the acceptable characters, 
    # then 'csinosins' would be acceptable.

    for s in words:
        if s in sx:
            sx=sx.replace(s,' ')
    for s in ops:
        if s in sx:
            sx=sx.replace(s,' ')
    for s in nums:
        if s in sx:
            sx=sx.replace(s,' ')
    for s in var:
        if s in sx:
            sx=sx.replace(s,' ')
    # at this point sx is only spaces and unnacceptable words
    # find the first non-space and return until there is a space
    for i in range(0,len(sx)):
        if sx[i] != ' ':
            j=i
            err=''
            while sx[j] != ' ':
                err=err+sx[j]
                j=j+1
            return err #returns first unnacceptable word
    return True


def ratio(summand):
    '''
    Flask-available function to calculate ratio test
    Parameters:
        summand (string): a summand to calculate the ratio test of
    Returns:
        list [int, message (string)]: A number to signify error type, and the error
        list [0, res(float)]: 0 to signify no error, and the result of the calculation
    '''
    seq=summand
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
            return[0,res]
    else:
        errorMessage = '"'+f+'"'+' is not an acceptable word/character'
        return [2,errorMessage]


@app.route('/ratioTest', methods=['POST', 'GET'])
def run():
    '''
    A flask endpoint to trigger ratio test calculation
    Expected payload:
        {
            summand: summand
        }
    '''
    print(request.args['summand'], file=sys.stdout)
    ss = request.args['summand']
    print(ss, file=sys.stdout)
    res = ratio(ss)
    message = ''
    if res[0] == 0: 
        if res[1] == 1:
            message = "Test inconclusive"
        elif res[1] < 1 :
            message = "Converges"
        elif res[1] > 1:
            message = "Diverges"
        return jsonify(result = message,
                       num = float(res[1])
        )
    elif res[0] == 1 or res[0] == 2:
        return jsonify(result = res[1],
                       num = 'Error:'
        )


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8000)

