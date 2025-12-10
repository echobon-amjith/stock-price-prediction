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
CREATE TABLE iocl_clean (
    date DATE,
    close decimal(10,2),
    log_close decimal(10,2)
);