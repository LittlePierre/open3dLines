#!/bin/bash


MESSAGES=`find . -name \*.py`

echo $MESSAGES

TMP_DIR=`mktemp -d`
echo $TMP_DIR


function get_messages()
{
#	PO_FILENAME=$1
#	$LANGUAGE=$1
	PO_FILENAME="Lines3DCAD"

	shift
	FILES=$*

	PO_FILE_WO_EXT=${BASE_MESSAGE_DIR}/$LANGUAGE/LC_MESSAGES/$PO_FILENAME
	PO_FILE=${PO_FILE_WO_EXT}.po
	PARSED_PO_FILE=${PO_FILE_WO_EXT}_parsed.po
	xgettext --sort-by-file --force-po -L python --from-code=utf-8 --add-comments -o $PARSED_PO_FILE $FILES
	if [ -e $PARSED_PO_FILE ] ; then
		sed --in-place s'/charset=CHARSET/charset=UTF-8/' $PARSED_PO_FILE
	fi
	if [ -e $PO_FILE ] ; then
		MERGED_PO_FILE=${PO_FILE_WO_EXT}_merged.po
#		sed --in-place s'/charset=CHARSET/charset=UTF-8/' $PARSED_PO_FILE
		sed --in-place s'/charset=CHARSET/charset=UTF-8/' $PO_FILE
		msgmerge -N --sort-output --no-wrap $PO_FILE $PARSED_PO_FILE > $MERGED_PO_FILE && mv $MERGED_PO_FILE $PO_FILE
		rm -f $PARSED_PO_FILE $MERGED_PO_FILE
	else
		mv $PARSED_PO_FILE $PO_FILE
	fi
	sed --in-place '/POT-Creation-Date/d' $PO_FILE
	sed --in-place '/^.*tmp\/tmp.*$/d' $PO_FILE
	if [ "`pocount --short $PO_FILE | awk '{print $4}'`" == "0" ]; then
		rm -f $PO_FILE
	fi
}



BASE_MESSAGE_DIR="./locale/"
LANGUAGES=`ls  ${BASE_MESSAGE_DIR}`
for LANGUAGE in $LANGUAGES
do
	echo $LANGUAGE
	get_messages $LANGUAGE $MESSAGES
	wait
done
wait

echo "First part Done"




