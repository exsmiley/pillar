# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 14:21:57 2017

@author: VL
"""
import requests
import pandas as pd
from bokeh.charts import Bar, Donut, show
from bokeh.models import HoverTool, SaveTool
from bokeh.embed import components

# comparing two senators
def compare_politicians(name1, name2, chamberName):
    """
    Compares politicians ("FirstName LastName", "FirstName LastName", house or senate)
    Politicians must be in the same chamber
    """
    api_key = "dNCaDByvPa8s2y9CjdNh15tDKOvQ3HS730R2GFJH"
    
    first_person = name1
    second_person = name2
    congress = 114
    chamber = chamberName
    id1 = ""
    id2 = ""
    comparison = {}
    comparison_df = pd.DataFrame(index = range(2), columns = ["Votes", "Number of Votes"])
    
    headers = {'X-API-Key': api_key}

    url = "https://api.propublica.org/congress/v1/%s/%s/members.json" % (congress, chamber)
    results = requests.get(url, headers = headers).json()["results"][0]

    # retrieve ids for the congress members    
    for r in results["members"]:
        if (r["first_name"] == first_person.split()[0] and r["last_name"] == first_person.split()[1]):
            id1 = r["id"]
        if (r["first_name"] == second_person.split()[0] and r["last_name"] == second_person.split()[1]):
            id2 = r["id"]

    url = "https://api.propublica.org/congress/v1/members/%s/votes/%s/%s/%s.json" % (id1, id2, congress, chamber)
    results = requests.get(url, headers = headers).json()["results"][0]
        
    for category in results:
        comparison[category] = [results[category]]
        
    common_votes = int(str(comparison["common_votes"][0]))
    disagree_votes = int(str(comparison["disagree_votes"][0]))
    agree_percent = float(str(comparison["agree_percent"][0]))
    disagree_percent = float(str(comparison["disagree_percent"][0]))
    
    comparison_series = pd.Series([agree_percent, disagree_percent], index = ["Agree", "Disagree"])

    comparison_df.set_value(index = 0, col = "Votes", value = "In Common")
    comparison_df.set_value(index = 1, col = "Votes", value = "Disagree")
    
    comparison_df.set_value(index = 0, col = "Number of Votes", value = common_votes)
    comparison_df.set_value(index = 1, col = "Number of Votes", value = disagree_votes)
    
    return comparison_df, comparison_series

comparison_df, comparison_series = compare_politicians("Tim Kaine", "Mark Warner", "senate")

hover = HoverTool(
    tooltips = [
    ("Number of Votes", "@height")
])

TOOLS = [SaveTool(), hover]

# plot = Bar(comparison_df, values = "Number of Votes", label=CatAttr(columns=['Votes'], sort = False), group='Votes', legend='top_right', color=ColorAttr(columns=['Votes']), tools="resize,hover,save")
barplot = Bar(comparison_df, values = "Number of Votes", label=CatAttr(columns=['Votes'], sort = False), group='Votes', legend='top_right', color='Votes', tools=TOOLS, ylabel = "Number of Votes")

for r in barplot.renderers:
    try:
        r.glyph.width = 1.15
    except AttributeError:
        pass
    
show(barplot)
script_barplot, div_barplot = components(barplot)

pie_chart = Donut(comparison_series, tools = "save")
show(pie_chart)
script_piechart, div_piechart = components(barplot)
