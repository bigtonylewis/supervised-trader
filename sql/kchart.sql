CREATE TABLE kchart_eurusd_1m(id serial, ts TIMESTAMP WITH TIME ZONE UNIQUE, open FLOAT, close FLOAT, high FLOAT, low FLOAT, volume int);
CREATE TABLE kchart_eurusd_5m(id serial, ts TIMESTAMP WITH TIME ZONE UNIQUE, open FLOAT, close FLOAT, high FLOAT, low FLOAT, volume int);
CREATE TABLE kchart_eurusd_60m(id serial, ts TIMESTAMP WITH TIME ZONE UNIQUE, open FLOAT, close FLOAT, high FLOAT, low FLOAT, volume int);
