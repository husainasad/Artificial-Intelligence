import pandas as pd
from math import sqrt
import csv
from scipy import stats

Layout = ['tiny', 'small','medium', 'big']
Search = ['dfs', 'bfs', 'ucs', 'astar,heuristic=manhattanHeuristic']

testheader = ['Map', 'Search Algorithm 1', 'Search Algorithm w', 'Mean Expanded Nodes using S1', 'Mean Expanded Nodes using S2', 'T-score', 'P-value']

with open('ttest_nodes_mm.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(testheader)
  f.close()

for l in Layout:

  data_items=[]

  df = pd.read_csv('finalresult.csv')
  df = df[df['Map'].str.contains(l)]
  df = df.drop('Map', axis=1)
  df = df.drop('Total Cost', axis=1)
  df = df.drop('Score', axis=1)

  df1 = df[df['Search Algorithm']=='mm,heuristic=manhattanHeuristic']
  df1 = df1.reset_index()
  df1 = df1.drop('index', axis=1)
  df1 = df1.drop('Search Algorithm', axis=1)
  df1 = df1.rename(columns={'Number of Nodes Expanded': 'mm'})
  col1 = df1['mm'].copy()

  for s in Search:

    df2 = df[df['Search Algorithm']==s]
    df2 = df2.reset_index()
    df2 = df2.drop('index', axis=1)
    df2 = df2.drop('Search Algorithm', axis=1)
    df2 = df2.rename(columns={'Number of Nodes Expanded': s})
    col2 = df2[s].copy()

    dfnew = df1.join(df2)
    dfnew.reset_index()

    a = dfnew['mm'].mean()
    b = dfnew[s].mean()

    data_items.append(l)
    data_items.append('mm')
    data_items.append(s)
    data_items.append(a)
    data_items.append(b)

    tscore, pval = stats.ttest_rel(col1, col2)

    data_items.append(tscore)
    data_items.append(pval)

    with open('ttest_nodes_mm.csv', 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(data_items)
      data_items = []
      f.close()

# temp = pd.read_csv('ttest_mm.csv')
# print(temp)

with open('ttest_nodes_mm0.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(testheader)
  f.close()

for l in Layout:

  data_items=[]

  df = pd.read_csv('finalresult.csv')
  df = df[df['Map'].str.contains(l)]
  df = df.drop('Map', axis=1)
  df = df.drop('Total Cost', axis=1)
  df = df.drop('Score', axis=1)

  df1 = df[df['Search Algorithm']=='mm']
  df1 = df1.reset_index()
  df1 = df1.drop('index', axis=1)
  df1 = df1.drop('Search Algorithm', axis=1)
  df1 = df1.rename(columns={'Number of Nodes Expanded': 'mm0'})
  col1 = df1['mm0'].copy()

  for s in Search:

    df2 = df[df['Search Algorithm']==s]
    df2 = df2.reset_index()
    df2 = df2.drop('index', axis=1)
    df2 = df2.drop('Search Algorithm', axis=1)
    df2 = df2.rename(columns={'Number of Nodes Expanded': s})
    col2 = df2[s].copy()

    dfnew = df1.join(df2)
    dfnew.reset_index()

    a = dfnew['mm0'].mean()
    b = dfnew[s].mean()

    data_items.append(l)
    data_items.append('mm0')
    data_items.append(s)
    data_items.append(a)
    data_items.append(b)

    tscore, pval = stats.ttest_rel(col1, col2)

    data_items.append(tscore)
    data_items.append(pval)

    with open('ttest_nodes_mm0.csv', 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(data_items)
      data_items = []
      f.close()

# temp = pd.read_csv('ttest_mm0.csv')
# print(temp)

with open('ttest_nodes_mm_mm0.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(testheader)
  f.close()

for l in Layout:

  data_items=[]

  df = pd.read_csv('finalresult.csv')
  df = df[df['Map'].str.contains(l)]
  df = df.drop('Map', axis=1)
  df = df.drop('Total Cost', axis=1)
  df = df.drop('Score', axis=1)

  df1 = df[df['Search Algorithm']=='mm,heuristic=manhattanHeuristic']
  df1 = df1.reset_index()
  df1 = df1.drop('index', axis=1)
  df1 = df1.drop('Search Algorithm', axis=1)
  df1 = df1.rename(columns={'Number of Nodes Expanded': 'mm'})
  col1 = df1['mm'].copy()
  
  df2 = df[df['Search Algorithm']=='mm']
  df2 = df2.reset_index()
  df2 = df2.drop('index', axis=1)
  df2 = df2.drop('Search Algorithm', axis=1)
  df2 = df2.rename(columns={'Number of Nodes Expanded': 'mm0'})
  col2 = df2['mm0'].copy()

  dfnew = df1.join(df2)
  dfnew.reset_index()

  a = dfnew['mm'].mean()
  b = dfnew['mm0'].mean()

  data_items.append(l)
  data_items.append('mm')
  data_items.append('mm0')
  data_items.append(a)
  data_items.append(b)

  tscore, pval = stats.ttest_rel(col1, col2)

  data_items.append(tscore)
  data_items.append(pval)

  with open('ttest_nodes_mm_mm0.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data_items)
    data_items = []
    f.close()

# temp = pd.read_csv('ttest_mm_mm0.csv')
# print(temp)