#!/usr/bin/env python
# encoding: utf-8
"""
recommend.py

Created by mmiyaji on 2012-11-28.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *
import pymongo
import pickle
import pygraphviz as pgv

class Recom():
    """
    """
    def __init__(self, memkey="nobel_word_network_limit100"):
        print memkey,cache.get(memkey)
        if memkey in cache:
            g,self.G = cache.get(memkey)
        else:
            try:
                self.G=pickle.load(open(os.path.join(settings.TMP_DIR,'nx.dump')))
            except:
                g,self.G = self.recalc_network(memkey)
                pickle.dump(self.G,open(os.path.join(settings.TMP_DIR,'nx.dump'),'w'))
#        for c,i in enumerate(self.G.nodes()):
#            self.get_path(i)
#            print c,i
    def get_network(self):
        """
        Arguments:
        - `self`:
        """
        return self.G
    def get_path(self, w1, w2 = ""):
        p = "netpath_%s" % w1
        if p in cache:
            return cache.get(p)
        else:
            length,path=nx.single_source_dijkstra(self.G, w1)
            cache.set(p, [length,path], 300000)
        if w2:
            return length[w2],path[w2]
        else:
            return length,path
    def recalc_network(self, memkey="nobel_word_network_limit100", memtime=0, netlim=3, edge_max=277095.0, span = 20000):
        G=nx.Graph()
        conn = pymongo.Connection(settings.MONGODB_PATH2, settings.MONGODB_PORT2)
        db = conn.rakuten
        usedb = eval("db.%s" % memkey)
        nets = usedb.find()
        count = nets.count()
        max = 0
        min = 999999
        for c,i in enumerate(nets):
            if c % 1000 == 0:
                print c+1,"/",count, i
            cc = float(i['count'])
            G.add_node(i['word01'])
            G.add_node(i['word02'])
            wei = 1.0-cc/edge_max
            if wei < 0:
                wei = 0
            G.add_edge(i['word01'],i['word02'], weight=wei)
        cache.set(memkey, G, memtime)
        return cache.get(memkey),G
    def draw(self, memkey="nobel_word_network_limit100", memtime=0, netlim=3, edge_max=277095.0, span = 20000, viewport='3000,2000,.1', out='pyg.png', prog='neato', maxnode=2000):
        dot = """
        graph pyg
        {
          graph [viewport="%s", resolution=72];
           }
            """ % viewport
        A = pgv.AGraph(string=dot)
        conn = pymongo.Connection(settings.MONGODB_PATH2, settings.MONGODB_PORT2)
        db = conn.rakuten
        usedb = eval("db.%s" % memkey)
        nets = usedb.find()
        count = nets.count()
        out = (os.path.join(settings.TMP_DIR, out))
        max = 0
        min = 999999
        for c,i in enumerate(nets):        
            if c % 1000 == 0:
                print c+1,"/",count, i
                if c > maxnode:
                    break
            cc = float(i['count'])
            A.add_node(i['word01'])
            A.add_node(i['word02'])
            wei = 1.0-cc/edge_max
            if wei < 0:
                wei = 0
            A.add_edge(i['word01'],i['word02'], weight=wei)
        A.layout(prog=prog)
        A.draw(out)
        # P = pgv.AGraph(d)
        # P.layout(prog='dot')
        # P.draw('pyg_ja.png')

def main():
    r = Recom()
    r.recalc_network()

if __name__ == '__main__':
    main()
    

