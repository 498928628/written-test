from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

main = Blueprint('index', __name__)

def linreg(X, Y):
    # Running the linear regression
    X = sm.add_constant(X)
    model = regression.linear_model.OLS(Y, X).fit()
    a = model.params[0]
    b = model.params[1]
    X = X[:, 1]
    # Return summary of the regression and plot results
    X2 = np.linspace(X.min(), X.max(), 100)
    Y_hat = X2 * b + a
    plt.cla()
    plt.scatter(X, Y, alpha=0.3) # Plot the raw data
    plt.plot(X2, Y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    # print('model',model.summary(),type(model.summary()))

    plt.savefig('cache.png')
    return model.summary()

@main.route("/")
def index():
    X = np.random.rand(100)
    X = X.tolist()
    X = map(str, X)
    X = ','.join(X)

    Y = np.random.rand(100)
    Y = Y.tolist()
    Y = map(str, Y)
    Y = ','.join(Y)
    return render_template("index.html",series1 = X, series2 = Y)


@main.route("/load", methods=['POST'])
def load():
    form = request.form
    list1_str = form['list1']
    list2_str = form['list2']
    t1 = list1_str.split(',')
    result1 = list(map(float,t1))
    X = np.array(result1)
    t2 = list2_str.split(',')
    result2 = list(map(float,t2))
    Y = np.array(result2)
    # print("xxxxxxxxxxx",linreg(X, Y),type(linreg(X, Y)))
    # try:
    #     os.remove('cache.png')
    # except:
    #     print('文件夹下没有cache.png')
    text = str(linreg(X, Y))
    with open('cache.txt', 'w') as file:
        file.write(text)
    return redirect(url_for('.register'))

@main.route("/register")
def register():
    fff = []
    with open('cache.txt') as file:
        ff = file.readlines()
        for line in ff:
            print(line)
            new = sort_line(line)
            fff.append(new)
    return render_template("register.html", uu = fff)


#txt的文本排版处理
def sort_line(line):
    list = ['R-squared','F-statistic','Prob (F-statistic)',
             'Log-Likelihood','AIC:','BIC:',
            'Durbin-Watson:','Jarque-Bera (JB)','Prob(JB)','Cond. No']
    new = 'error'
    for i in list:
        if i in line:
            x = '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  ' + i
            new = line.replace(i,x)
    if new == 'error':
        return line
    else:
        return new


