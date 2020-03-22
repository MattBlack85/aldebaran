latest_data_query = """
SELECT country, total_cases, total_deaths FROM corona WHERE report_datetime = CURRENT_DATE OR report_datetime = CURRENT_DATE - 1 ORDER BY country;
"""

countries_by_day_query = """
SELECT country, total_cases, total_deaths, new_cases, new_deaths FROM corona WHERE report_datetime = :day ORDER BY country;
"""

countries_by_month_query = """
SELECT extract(month from report_datetime) as month, country, SUM(total_cases) AS tc, SUM(total_deaths) AS td, SUM(new_cases) AS nc, SUM(new_deaths) AS nd FROM corona WHERE extract(month from report_datetime) = :month GROUP BY country, month
ORDER BY country;
"""

country_list_query = """
SELECT DISTINCT country from corona ORDER BY country;
"""

country_data_query = """
SELECT report_datetime, total_cases, new_cases, total_deaths, new_deaths FROM corona WHERE country = :country ORDER BY report_datetime;
"""

all_data_query = """
select country, json_agg(json_build_object('total_deaths',total_deaths, 'new_deaths',new_deaths, 'total_cases',total_cases, 'new_cases',new_cases,'date',date(report_datetime))) as data from corona group by country;
"""

latest_data_by_region_query = """
SELECT t2.name AS region, SUM(total_deaths) as total_deaths, SUM(total_cases) AS total_cases FROM corona as t1 LEFT JOIN regions as t2 ON t2.type = t1.region WHERE report_datetime = CURRENT_DATE OR report_datetime = CURRENT_DATE - 1
 GROUP BY region, t2.name;
"""

region_data_by_day_query = """
SELECT report_datetime as time, t2.name AS region, SUM(total_deaths) as total_deaths, SUM(total_cases) AS total_cases
FROM corona as t1 LEFT JOIN regions as t2 ON t2.type = t1.region
GROUP BY t2.name, time ORDER BY time;
"""
