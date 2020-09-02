#!/bin/bash
HAVE_FILE=1

if [ ! -d urls-dir ];then
	echo "Please create urls-dir and put urls in urls-dir!"
	exit 1
fi

if [ ! -d urls-finish-dir ];then
	mkdir -pv urls-finish-dir
fi

while [ $HAVE_FILE -eq 1 ]
do
	url_txt=`ls urls-dir`
	if [ Z"$url_txt" == Z ];then
		break
	fi

	for url_name in $url_txt
	do
		bash run.sh $url_name
		mv -v urls-dir/$url_name urls-finish-dir/
	done
done
