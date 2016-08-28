
#!/usr/bin/bash

# 3 args needed:
# $1: data folder
# $2: start year to download
# $3: end year to download
# Example: bash download.sh data_folder/ 2003 2016

mkUdir () {

	if [ ! -d  $1 ]; then
		mkdir -p $1
	fi
}

fetchFiles () {

	files=($(curl $1 --stderr - | grep -o 'href="[^"]*zip' | grep -oP "(?<=href=).*" | grep -oP "(?<=\.\\\\).*"))
	echo ${files[@]}
}


download () {
	curl --fail -O $1
}

CWD=$(pwd)

DATA_PATH=$CWD"/"$1

mkUdir $DATA_PATH
cd $DATA_PATH

months=("01%20January" "02%20February" "03%20March" "04%20April" "05%20May" "06%20June" "07%20July" "08%20August" "09%20September" "10%20October" "11%20November" "12%20December")

years=($(seq $2 $3))

mainlink=http://ratedata.gaincapital.com


for y in ${years[@]}; do
	for m in ${months[@]}; do
		url_months=$mainlink"/"$y"/"$m"/"
		
		files=($(fetchFiles $url_months))

		for i in ${files[@]}; do
			url=$mainlink"/"$y"/"$m"/"$i
			pair=($(echo $i | cut -c1-7))
			folder=$DATA_PATH"/"$pair
			mkUdir $folder
			cd $folder
			tmp_folder=$folder"/tmp_folder"
			mkUdir $tmp_folder
			cd $tmp_folder
			digitm=$( echo $m | cut -c1-2)
			filename=$y"_"$digitm"_"$i
			curl --fail -s $url --output $filename
			echo $i
			cd $folder
		done
	done
	echo "<==========================================>"
done
