select pg_stat_statements_reset();
 
 
select pg_stat_statements_info();


pg_stat_statements.track = 'all'

SELECT now(), d.datname , queryid, s.calls, 
round(s.min_exec_time) min_exec_time, 
round(s.mean_exec_time) mean_exec_time, 
round(s.max_exec_time) max_exec_time, 
round(s.stddev_exec_time) stddev_exec_time, 
query
FROM pg_stat_statements s
JOIN pg_database d ON s.dbid = d.oid
WHERE calls > 2
ORDER BY s.total_exec_time DESC;



--- https://explain.dalibo.com <- view execution plan
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)
--- query here