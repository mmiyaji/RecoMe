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
    def __init__(self, memkey="nobel_word_network_limit100", netlim=0):
        print memkey,cache.get(memkey)
        if memkey in cache:
            g,self.G = cache.get(memkey)
        elif settings.GRAPH and settings.GRAPH_KEY == memkey:
            self.G = settings.GRAPH
        else:
            try:
                self.G=pickle.load(open(os.path.join(settings.TMP_DIR,'nx'+memkey+'.dump')))
            except:
                g,self.G = self.recalc_network(memkey, netlim=netlim)
                pickle.dump(self.G,open(os.path.join(settings.TMP_DIR,'nx'+memkey+'.dump'),'w'))
            if not settings.GRAPH:
                print 'cache GRAPH', memkey
                settings.GRAPH_KEY = memkey
                settings.GRAPH = self.G
#        for c,i in enumerate(self.G.nodes()):
#            self.get_path(i)
#            print c,i
    def get_network(self):
        """
        Arguments:
        - `self`:
        """
        return self.G
    def is_node(self, w):
        if w in self.G.node:
            return True
        else:
            return False
    def get_path(self, w1, w2 = ""):
        p = "netpath_%s_%s" % (w1, w2)
        # if p in cache:
        #     return cache.get(p)
        # else:
        if True:
            if self.is_node(w1) and self.is_node(w2):
                length,path=nx.single_source_dijkstra(self.G, w1)
                if w2 in path:
                    cache.set(p, [length[w2],path[w2]], 300000)
                    return length[w2],path[w2]
                else:
                    cache.set(p, [0,[w1,w2]], 300000)
                    return 0,[w1,w2]
            else:
                cache.set(p, [0,[w1,w2]], 300000)
                return 0,[w1,w2]
        # if w2:
        #     return length[w2],path[w2]
        # else:
        #     return length,path
    def get_neighbors(self, w):
        return self.G.neighbors(w)
    def delete_path(self, w1, w2):
        """
        Arguments:
        - `self`:
        - `w1`:
        - `w2`:
        """
        # print 'delete edge ',w1,w2,
        # if self.is_node(w1) and self.is_node(w2):
        if True:
            if self.G.get_edge_data(w1,w2):
                value = self.G.get_edge_data(w1,w2)['weight']
                self.deleted_path = [w1, w2, value]
                self.G.remove_edge(w1, w2)
                return True
            else:
                return False
        else:
            return False
    def repair_path(self):
        d = self.deleted_path
        self.G.add_edge(d[0],d[1],weight=d[2])

    def recalc_network(self, memkey="nobel_word_network_limit100", wordmemkey="nobel_word", memtime=0, netlim=0, edge_max=277095.0, span = 20000):
        print 'recalc network',memkey
        G=nx.Graph()
        conn = pymongo.Connection(settings.MONGODB_PATH2, settings.MONGODB_PORT2)
        db = conn.rakuten
        usedb = eval("db.%s" % memkey)
        nets = usedb.find()
        count = nets.count()
        print 'count',count
        max = 0
        min = 999999
        if not netlim:
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
        else:
            worddb = eval("db.%s" % wordmemkey)
            words = worddb.find()
            word_count = words.count()
            for c,w in enumerate(words):
                try:
                    n1 = usedb.find({'word01':w["word"]}).sort('count', pymongo.DESCENDING)[0]
                    n2 = usedb.find({'word02':w["word"]}).sort('count', pymongo.DESCENDING)[0]
                    if c % 1000 == 0:
                        print c+1,"/",count
                    cc1 = float(n1['count'])
                    G.add_node(n1['word01'])
                    G.add_node(n1['word02'])
                    wei = 1.0-cc1/edge_max
                    if wei < 0:
                        wei = 0
                    G.add_edge(n1['word01'],n1['word02'], weight=wei)
                    cc2 = float(n2['count'])
                    G.add_node(n2['word01'])
                    G.add_node(n2['word02'])
                    wei = 1.0-cc2/edge_max
                    if wei < 0:
                        wei = 0
                    G.add_edge(n2['word01'],n2['word02'], weight=wei)
                except:
                    print "error"
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


