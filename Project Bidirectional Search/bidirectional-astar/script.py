import os 
import csv
import pandas as pd

# layout_items = ['tinyMaze', 'smallMaze', 'mediumMaze', 'bigMaze']
layout_items = []
maze_names = ['tiny', 'small', 'medium', 'big']
for i in maze_names:
  for j in range(20):
    layout_items.append(i+str(j))

# print(layout_items)
algo_items = ['dfs', 'bfs', 'ucs', 'astar,heuristic=manhattanHeuristic','mm', 'mm,heuristic=manhattanHeuristic']

# resultheader = ['Map', 'Search Algorithm', 'Total Cost', 'Number of Nodes Expanded', 'Score']
resultheader = ['Map', 'Search Algorithm']
with open('results.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(resultheader)
  f.close()

scoreheader = ['Score']
with open('scores.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(scoreheader)
  f.close()

nodeheader = ['Total Cost', 'Number of Nodes Expanded']
with open('costs.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(nodeheader)
  f.close()

for i in layout_items:
  for j in algo_items:
    # print('pacman.py -l '+i+' -z .5 -q -p SearchAgent -a fn='+j)
    # print("Layout: "+ i + "Algorithm: "+ j)
    data_items = []
    data_items.append(i)
    data_items.append(j)
    s = 'pacman.py -l '+i+' -z .5 -q -p SearchAgent -a fn='+j
    print(s)
    os.system('python '+s)
    with open('results.csv', 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(data_items)
      f.close()



df1 = pd.read_csv('results.csv')
df2 = pd.read_csv('costs.csv')
df3 = pd.read_csv('scores.csv')
df1 = df1.join(df2)
df1.reset_index()
df1 = df1.join(df3)
df1.reset_index()
df1.to_csv('finalresult.csv', encoding='utf-8', index=False)