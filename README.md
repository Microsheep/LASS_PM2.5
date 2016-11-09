# LASS_PM2.5
#### Some useful code for 2016 NCTU DataMining Course
#### If you find a BUG, Open an Issue! Pull requests are also Welcomed!

## PM2.5_data_pre_process
This is a folder which contains a python3 code for pre-processing all the raw data from the MQTT servers.

### How to use it?
- Download the Data Logs from the MQTT server: 
[How to get data log from server](https://lass.hackpad.com/How-to-get-data-log-from-server-Ztu9mpUsGL9)
- Create a table in you mysql database using [create_table.sql](https://github.com/Microsheep/2016_NCTU_DataMining_Course/blob/master/PM2.5_data_pre_process/create_table.sql)
- Run [PM2.5_data_convert.py](https://github.com/Microsheep/2016_NCTU_DataMining_Course/blob/master/PM2.5_data_pre_process/PM2.5_data_convert.py) using python3, configure DATA_RANGE if you want to use a custom range
- The CSV file will be generated and you can easily load it into mysql

### Other information

- [LASS - Data specification](https://lass.hackpad.com/LASS-Data-specification-1dYpwINtH8R)
##### Many of the data in the MQTT server are not following the specs and there are lots of corrupted data. I tried to save as many data I can confidently correct, and discard any other corrupted data.

- [20160801_to_20160925_attibutes.txt](https://github.com/Microsheep/2016_NCTU_DataMining_Course/blob/master/PM2.5_data_pre_process/20160801_to_20160925_attibutes.txt) is a file which contains the attributes found using another code.
##### Total Corrupted in this file only counts those that has a bad key in one of the attributes in the raw data, which the corrupted data is then discarded. While the real data generation will also discard data that its value is not valid.

### Data Download

- FULL_DATA: 20160801 ~ 20160925 / about 2.6 GB [Download](https://goo.gl/Z8QBlX)
##### MD5:a87689ca4aff0eac5ec2440669363d53 / Row count(wc -l):15975871

- HW_DATA: 20160918 ~ 20160925 / about 400 MB [Download](https://goo.gl/JHwTDE)
##### MD5:1cbaa80d70f96a3794cd8c77ae7fa607 / Row count(wc -l):2341175
