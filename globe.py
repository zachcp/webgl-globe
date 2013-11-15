# -*- coding: utf-8 -*-
"""
Simple App to Create A GLobe Using
https://github.com/dataarts/webgl-globe
as a starting point

    :copyright: (c) 2012 by Zach Charlop-Powers.
"""

import os, ast, json
from flask import Flask, render_template, jsonify
from flask_frozen import Freezer
from pandas import read_csv, DataFrame

#flask app
app = Flask(__name__)
app.config.update(FREEZER_BASE_URL = "/~zachpowers")
freezer = Freezer(app)

@app.route('/')
def index():
    data = json.load( open('static/population909500.json', 'r') )
    print data
    return render_template('index.html',
                            data = json.dumps(data) )


if __name__ == '__main__':
    #freezer.freeze()
    app.debug = True
    app.run()