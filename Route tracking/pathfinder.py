#!/usr/bin/env python

node_name = {}
with open("nodes.txt", encoding = 'utf-8') as f:
   file = f.read()
   lines = file.split("\n")
   for l in lines:
       name = l.split(" ")[0]
       code = l.split(" ")[6].split("=")[1].replace("\"", "")
       node_name[name] = code     
node_name["000"] = ""    
       
graph = {}
with open("routes.txt", encoding = 'utf-8') as f:
   file = f.read()
   lines = file.split("\n")
   for l in lines:
        path = l.split(" ")[0]
        a,b = path.split("->")
        if a not in graph:
            graph[a] = [b]
        else:
            graph[a] = graph[a] + [b]


def depth_search(actual_node, visited, message):
    actual_visited = visited.copy()
    actual_visited.add(actual_node)
    if message.startswith("FLAG{") and message.endswith("}") and len(message) == 25:
        print(message)

    for next in graph.get(actual_node):
        if (next not in actual_visited):   
                depth_search(next, actual_visited.copy(), message+node_name.get(next))

depth_search("000", set(), "")   