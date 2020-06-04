"""
Filtro colaborativo sobre Neo4j
"""
from py2neo import Graph, Node, NodeMatcher
import connexion

class FiltroColaborativo():        

  def getRecCollab(self, userid, n):
    USERNAME = "neo4j"
    PASS = "Grupo06" #default
    graph = Graph("bolt://localhost:7687", auth = (USERNAME, PASS))
    print ("Usuario " + userid)
    rec = graph.run('MATCH (u1:User {id:$userid})-[r:RATED]->(m:Movie) '
                    'WITH u1, avg(r.rating) AS u1_mean '
                    'MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2) '
                    'WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) '
                    'WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings '
                    'UNWIND ratings AS r '
                    'WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom, '
                    'sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom, u1, u2 WHERE denom <> 0 '
                    'WITH u1, u2, nom/denom AS pearson '
                    'ORDER BY pearson DESC LIMIT 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) ) '
                    'RETURN m.title AS title, SUM( pearson * r.rating) AS score '
                    'ORDER BY score DESC LIMIT toInteger($n);', userid=userid, n=n)
    print (rec.data())

    return rec.data()
