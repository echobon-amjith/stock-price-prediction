alter table iocl
change column `('Date', '')` `date` date,
change column `('Open', 'IOC.NS')` `open` decimal(10,2),
change column `('High', 'IOC.NS')` `high` decimal(10,2),
change column `('Low', 'IOC.NS')` `low` decimal(10,2),
change column `('Close', 'IOC.NS')` `close` decimal(10,2),
change column `('Volume', 'IOC.NS')` `volume` bigint,
add column log_close decimal(10,2),
add column forecast decimal(10,2);
update iocl
set log_close = log(close);
