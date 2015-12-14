#!/bin/bash

pushd /home

# data di oggi
DATE_TAG=`date +%Y%m%d`

# bucket s3 con i dump
BUCKET_NAME=open_aid

echo dumping postgres database ...
pg_dump --clean -Upostgres open_aid | gzip > pg_dump.gz

echo dumping solr index files ...
tar cvzf solr_dump.tgz solr/data/*

echo dumping media directory ...
tar cvzf media_dump.tgz open_aid/resources/media/*

echo sending dumps to s3 in s3://$BUCKET_NAME/daily/$DATE_TAG/
s3cmd put *_dump.*gz s3://$BUCKET_NAME/daily/$DATE_TAG/

echo removing dumps
rm *_dump.*gz

echo removing dumps older than a week
for (( i=15; i>=7; i-- ));
do
  s3cmd del --recursive s3://$BUCKET_NAME/daily/`date -d "-$i days" +"%Y%m%d"`/
done;

popd
