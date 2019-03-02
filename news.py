# !/usr/bin/env python3
import psycopg2
from datetime import datetime

dbName = "news"
first_1 = """
SELECT articles.title,
     count(*)
FROM log,
   articles
WHERE log.path = '/article/' || articles.slug
GROUP BY articles.title
ORDER BY count(*) DESC
LIMIT 3;
"""

secnd_2 = """
SELECT authors.name,
     count(*)
FROM log,
   articles,
   authors
WHERE log.path = '/article/' || articles.slug
GROUP BY authors.name
ORDER BY count(*) DESC;
"""

third_3 = """
SELECT total.day,
ROUND(((errors.error_requests*1.0) / total.requests), 3)
AS percent
        FROM (
              SELECT date_trunc('day', time) "day", count(*) AS error_requests
              FROM log
              WHERE status LIKE '404%'
              GROUP BY day
              ) AS errors
              JOIN(
              SELECT date_trunc('day', time) "day", count(*) AS requests
              FROM log
              GROUP BY day)
              AS total
              ON total.day=errors.day
              WHERE (ROUND((
              (errors.error_requests*1.0) / total.requests), 3) > 0.01)
              ORDER BY persent DESC;
"""


def results(query):
    con = psycopg2.connect("dbname={}".format(dbName))
    cur = con.cursor()

    try:
        cur.execute(query)
    except Exception as e:
        print(e)
    else:
        return cur.fetchall()
    finally:
        con.close()


def print_results(query_results):
    for i, res in enumerate(query_results):
        print("\t"+str(i+1)+"."+str(res[0])+" - "+str(res[1])+" views")


def print_errors(query_results):
    for result in query_results:
        date = result[0]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = datetime.strftime(date_obj, "%B %d,%Y")
        print("\t"+str(formatted_date)+" - "+str(result[1])+"% errors")


if __name__ == '__main__':
    print("What are the most popular three articles of all time?")
    articles = results(first_1)
    print_results(articles)
    print("%"*70)

    print("Who are the most popular article authors of all time?")
    authors = results(secnd_2)
    print_results(authors)
    print("%"*70)

    print("On which days did more than 1% of requests lead to errors?")
    error_days = results(third_3)
    print_errors(error_days)
    print("-"*50)
