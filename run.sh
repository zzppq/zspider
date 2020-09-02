#!/bin/bash
usage()
{
  echo 'bash run.sh <url-txt>'
  echo 'url-txt : 例如os_zhongbiao_xxx.txt格式'
}

if [ $# -ne 1 ];then
	usage
	exit 0
fi

URL_NAME=$1
DIR1=`echo $URL_NAME | cut -d _ -f 1`
DIR2=`echo $URL_NAME | cut -d _ -f 2`
DIR3=`echo $URL_NAME | cut -d _ -f 3`
if [ Z$DIR3 == Z ];then
	BASEDIR=`basename $DIR2 .txt`
	DIRPATH=lib/$DIR1/$BASEDIR
	mkdir -pv $DIRPATH
else
	BASEDIR=`basename $DIR3 .txt`
	DIRPATH=lib/$DIR1/$DIR2/$BASEDIR
	mkdir -pv $DIRPATH
fi

for line in `cat urls-dir/$1`
do
	python check_db.py --proname `basename $line` --prourl $line
	if [ $? -eq 1 ];then
		python Zspider.py --baseurl $line --destdir $DIRPATH
	fi
done
