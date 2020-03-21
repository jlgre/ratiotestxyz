#!/usr/bin/python3
import sympy
from sympy import sympify
from sympy import *
import sys

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


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
            errorMessage = inst.args[0]
            return [1, errorMessage]
        else:
            # computes the ratio and limit
            res=limit(seq/seq.subs(n,n-1),n,oo)
            return[0,res]
    else:
        errorMessage = 'Parse error: \'' + f + '\' is not acceptable input'
        return [2, errorMessage]

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(50))

    def __repr__(self):
        return '<Testimonial %r>' %self.id

@app.route('/', methods=['POST','GET'])
def index():
    tests = Testimonial.query.order_by(Testimonial.date_created).all()
    summand=''
    message='waiting...'
    if request.method == 'POST':
        summand=request.form['summand']
        result=ratio(summand)
        if result[0]==0:
            if result[1] < 1:
                message = 'Ratio=' + str(result[1]) + '. Series converges.'
            elif result[1] == 1:
                message = 'Ratio=' + str(result[1]) + '. Test inconclusive.'
            else:
                message = 'Ratio=' + str(result[1]) + '. Series diverges.'
            return render_template('index.html', message=message, oldsum=summand, tests=tests)
        else:
            message = result[1]
            return render_template('index.html', message=message, summand=summand, tests=tests)
    else:
        return render_template('index.html', message=message, summand=summand, tests=tests)

@app.route('/testimonial/', methods=['POST','GET'])
def testimonial():
    if request.method == 'POST':
        testc=request.form['story']
        testau=request.form['author']
        newt = Testimonial(content=testc, author=testau)
        try:
            db.session.add(newt)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error 405'
    else:
        return render_template('testimonial.html')

if __name__ == '__main__':
    app.run(debug=True)