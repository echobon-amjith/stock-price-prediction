CREATE TABLE iocl_clean (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE
);
DELIMITER |

CREATE PROCEDURE fill_dates(date_start DATE, date_end DATE)
BEGIN
    WHILE date_start <= date_end DO
        INSERT INTO iocl_clean (date) VALUES (date_start);
        SET date_start = DATE_ADD(date_start, INTERVAL 1 DAY);
    END WHILE;
END;
|

DELIMITER ;

CALL fill_dates('2007-04-02', '2025-11-23');

alter table iocl_clean
add column `close` decimal(10,2);

update iocl_clean as t1
left join iocl as t2 on t1.date = t2.date
set t1.close = t2.close;

UPDATE iocl_clean
SET close = (@n := COALESCE(close, @n))
ORDER BY date;

SELECT
    SUM(CASE WHEN close IS NULL THEN 1 ELSE 0 END) AS missing_close
FROM iocl_clean;