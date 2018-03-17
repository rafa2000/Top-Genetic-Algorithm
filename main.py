import numpy as np
import yaml
import datetime
from github import Github
from terminaltables import AsciiTable
from terminaltables import GithubFlavoredMarkdownTable
import pickle
import codecs

# Insert you username and password
with open('parameters.yml', 'r') as input:
    try:
        p = yaml.safe_load(input)
        # Make sure it is reading ok
        # print("user: %s" % p["user"])
        # print("password: %s" % p["password"])
    except yaml.YAMLError as error:
        print( error )
        exit(1)
g = Github(p["user"], p["password"])

number_of_reps = p["items"]
names_of_props = ["Id", "Name", "Description", "Language", "Stars", "Forks"]
github_server_link = "https://github.com/"
last_tables_file_name = 'last_table_data.pickle'
md_file_name = 'readme.md'

# Main query
seach_query = g.search_repositories(p["search"], sort="stars", order="desc")
results = []
for index, rep in enumerate(seach_query):

    # print(rep.url)  # Everything are here as json file (You can use it instead of the API)

    rep_prop = [index+1]
    link = github_server_link + rep.full_name
    rep_prop.append("[{}]({})".format(rep.name, link))
    rep_prop.append(rep.description)
    rep_prop.append(rep.language)
    rep_prop.append(rep.stargazers_count)
    rep_prop.append(rep.forks)

    results.append(rep_prop)

    if(index > number_of_reps-2):
        break

# Creating the table
table_data = [["" for x in range(len(names_of_props))] for y in range(number_of_reps + 1)]

for i in range(len(names_of_props)):
    table_data[0][i] = names_of_props[i]

for i in range(number_of_reps):
    for j in range(len(names_of_props)):
        table_data[i+1][j] = results[i][j]

# Saving Table data (For further analysis)
with open(last_tables_file_name, 'wb') as handle:
    pickle.dump(table_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Generating the ascii table
table = GithubFlavoredMarkdownTable(table_data)
table_str = table.table

# Writing the md file
with codecs.open(md_file_name, "w", "utf-8") as f:
    now = datetime.datetime.now()
    f.write("# Top %s Github repositories\n" % p["search"])
    f.write("Based on [Top Deep Learning](http://github.com/mbadry1/Top-Deep-Learning)<br /><br />\n")
    f.write("Here is a list of the top-%s %s Github repositories sorted by the number of stars.\n" % (p["items"], p["search"]))
    f.write("The query that has been used for the GitHub search API is \"%s" % p["search"] + "\".\n")
    f.write("<br /><br />\n")
    f.write("Date: %s\n" % now.strftime("%m/%d/%Y"))
    f.write("<br /><br />\n")
    f.write("Note: This listing will be updated regularly.\n")
    f.write("<br /><br />\n\n")
    f.write(table_str)
