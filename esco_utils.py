from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Graph
from rdflib import URIRef,BNode, Literal
import numpy as np

class ESCOUtil:
  def __init__(self, endpoint='http://vasco.ijs.si:22222/esco/query'):
    s = SPARQLStore(endpoint,context_aware=False)
    self.sg = Graph(store=s)#, identifier=config.DEFAULT_GRAPH_URI)

  def getSkills(self, subject):
      return self.traverse(subject,URIRef('http://data.europa.eu/esco/model#relatedEssentialSkill'),False)

  def broader(self, subject, predicate=URIRef('http://www.w3.org/2004/02/skos/core#broader')):
      return self.traverse(subject, predicate)

  def traverse(self, subject, predicate, recursive=True):
      objs = list(self.sg.objects(subject=subject, predicate=predicate))
      final_ret = set(objs)
      for obj in objs:
          lab = self.sg.preferredLabel(subject=obj, lang='sl')
          if recursive:
              final_ret = final_ret.union(self.traverse(obj, predicate))

      return final_ret

  def skills_up_graph(self, subject):
      occ_res = self.broader(subject)
      res = self.getSkills(subject)
      for r in occ_res:
          res = res.union(self.getSkills(r))
      return res

  def compare_metric_max_overlap(self, occ1, occ2):
      r1 = list(self.skills_up_graph(occ1))
      r2 = list(self.skills_up_graph(occ2))
  #     print(len(r1),len(r2))
      return len(np.setdiff1d(r1,r2)), len(np.setdiff1d(r2,r2))

  def get_all_skills_SKP2ESCO(self, df, skp_code):
        union_res = np.array([])
#         who = df['SKP koda-6'] == skp_code
#         print(who)
        for uri in df[df['SKP koda-6'] == skp_code]['URI'].unique():
#             print(uri)
            res = list(self.skills_up_graph(URIRef(uri)))
            union_res = np.union1d(res,union_res)

        return union_res
