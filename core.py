# -*- coding: utf-8 -*-
"""

Core: The core functionality for Globe Py to Interact with the Globe

"""
from __future__ import (print_function, division)
import random
import json
from pkg_resources import resource_string
from string import Template

import pandas as pd

GLMATRIX_SRC = "http://astrojs.s3.amazonaws.com/ruse/examples/lib/gl-matrix.js"
RUSE_SRC = "http://astrojs.s3.amazonaws.com/ruse/dist/ruse.js"

class Globe(object):
    """Top level Feint chart"""

    def __init__(self, data=None, lat=None, lon=None, group=None, var=None):
        """Initialize webgl Globe

        Parameters
        ----------
        data: Pandas DataFrame
        lat: string, default None
            DataFrame column for latitude column
        lon: string, default None
            DataFrame column for longitude column
        var: string, scale_factor default None
            DataFrame column for scaling the vertical columns
        group: string, default None
            DataFrame column reprenting groups

        Output
        ------
        Binds data to wegGL globe
        """
        if not isinstance(data, (pd.DataFrame, pd.Series)):
            raise ValueError(
                "Data must be a Pandas DataFrame or Series"
                )


        ### ToDo: check for columns named "lat, Latitude, etc."
        if not lat:
            raise ValueError("latitude column must be provided)
        else:
            self.lat = lat
        if not lon:
            raise ValueError("longitude column must be provided)
        else:
            self.lon = lon
        if not val:
            raise ValueError("value column must be provided)
        else:
            self.val = val

        if group is None:
            self.webgl_titles = "data"
            webgl_data = ["data"]
            for i,row in data.iterrows():
                webgl.append(row[lat])
                webgl.append(row[lon])
                webgl.append(row[val])
            self.webgl_data  = webgl_data
        else:
            self.webgl_titles = list( data[group].unique() )
            webgl_data = []
            for name, grouping in data.groupby(group):
                temp = [name]
                for i,row in grouping.iterrows():
                     temp.append(row[lat])
                     temp.append(row[lon])
                     temp.append(row[val])
                webgl_data.append(temp)
            self.webgl_data = webgl_data

    def display(self):
        """Display a webgl Globe in the IPython notebook"""
        from IPython.core.display import HTML
        from IPython.core.display import Javascript
        from IPython.core.display import display

        id = random.randint(0, 2 ** 16)

        Detector = str(resource_string('webglGlobe', 'Detector.js'))
        three    = str(resource_string('webglGlobe', 'three.js'))
        Tween    = str(resource_string('webglGlobe', 'Tween.js'))

        js = """
        require(["{0}"], function(glmatrix) {{
            window.mat4 = glmatrix.mat4;
            window.vec3 = glmatrix.vec3;
            console.log(glmatrix);
            $.getScript('{1}',function(){{
                console.log(ruse)
                var chart_element = $("#vis{2}");
                var r = new ruse(chart_element[0], 800, 500);
                r.plot({3});
            }})
        }});""".format(
            GLMATRIX_SRC, RUSE_SRC, id, self.ruse_data.to_json(orient='records')
            )
        a = HTML(
            '<div id="vis%d" style="height: 500px; width: 800px"></div>' % id)
        b = Javascript(js)
        display(a, b)

    def to_template(self, json_path='ruse.json',
                    html_path='feint_template.html'):
        """Export to simple HTML scaffold

        Parameters
        ----------
        json_path: string, default 'ruse.json'
            Path to write JSON data
        html_path: string, default 'feint_template.html'
            Path to write HTML

        Output
        ------
        JSON with webgl Globe-compatible data
        HTML scaffold
        """

        template = Template(
                str(resource_string('feint', 'feint_template.html'))
                )
        with open(html_path, 'w') as f:
            f.write(template.substitute(json_path=json_path))

        self.ruse_data.to_json(json_path, orient='records')
