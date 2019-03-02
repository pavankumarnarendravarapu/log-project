# !/usr/bin/env python3
import psycopg2
dbName = "news"
first_1 = """
SELECT articles.title, count(*)
FROM log, articles
WHERE log.path = '/article/' || articles.slug
GROUP BY articles.title
ORDER BY count(*) DESC
LIMIT 3;
"""
second_2 = """
SELECT authors.name, count(*) AS views 
FROM articles inner
JOIN authors ON articles.author = authors.id INNER JOIN log
ON log.path LIKE concat('%', articles.slug, '%') 
WHERE log.status LIKE'200'
GROUP BY authors.name
ORDER BY views DESC;
"""

third_3 = """
WITH requests AS (
SELECT time::date AS day,count(*)
FROM log
GROUP BY time::date
ORDER BY time::date
), err AS (
SELECT time::date AS day,count(*)
FROM log
WHERE status != '200 OK'
GROUP BY time::date
ORDER BY time::date
), erra AS (
SELECT requests.day ,
err.count::float /requests.count::float *100
AS ers
FROM requests,err
WHERE requests.day = err.day
)
SELECT * FROM erra WHERE ers > 1;
"""


def connect(dbName):
    try:
        data = psycopg2.connect("dbname={}".format(dbName))
        cur = data.cursor()
        return data, cur


"""def article(queries):
    data, cur = connect(dbName)
    cur.execute(first_1)
    results = cur.fetchall()
    for res in results:
        print('-> {title} @ {count} views'.format(title=res[0], count=res[1]))
    cur.close()
    data.close()"""

 def que_res(query):
 	data, cursor = connect()
 	cursor.execute(query)
 	return cursor.fetchall()
 	data.close()


def que_res(res):
    data, cur = connect(dbName)
    cur.execute(second_2)
    results = cur.fetchall()
    for index, res in enumerate(res[0]):
        print(
        	"\t", index+1, "@", res[0],
        	"\t - ", str(res[1]), "views")
    cur.close()
    data.close()


def error(res):
    data, cur = connect(dbName)
    cur.execute(third_3)
    results = cur.fetchall()
    for res in results:
        print(
            '-> {date:%B %d, %Y} @ {erra:.1f}% errors'.
            format(date=res[0], erra=res[1]))
        cur.close()
        data.close()

if __name__ == '__main__':
    firstqn = "1.What are the most popular three articles of the time?"
    secqn = "2.Who are the most popular article authors of all time?"
    thirdqn = "3.On which days did more than 1% of requests lead to errors?"
    print(firstqn)
    articleop = que_res(first_1), firstqn
    print(secqn)
    authorop = que_res(second_2), secqn
    print(thirdqn)
    errorop = error(third_3), thirdqn
