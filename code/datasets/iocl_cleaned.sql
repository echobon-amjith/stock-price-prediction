CALL fill_dates(date_sub(current_date(), interval 10 year), current_date());

update iocl_clean as t1
left join iocl as t2 on t1.date = t2.date
set t1.close = t2.close;

UPDATE iocl_clean
SET close = (@n := COALESCE(close, @n)),
 log_close = log(close)
ORDER BY date;

SELECT
    SUM(CASE WHEN close IS NULL THEN 1 ELSE 0 END) AS missing_close
FROM iocl_clean;