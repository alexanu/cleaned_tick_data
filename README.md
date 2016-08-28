# How to use this repo
1. Run __download.sh__. This file needs 3 args: your_data_folder, start_year, and end_year
2. Wait for the data is completely download to your directory. ( This may take a while. Go out, run, then come back)
3. Run __process.py__. This file needs 1 arg: your_data_folder (assuming the data download using download.sh)
4. Grab a cup of coffee, and relax.

### Example 

```
bash download.sh your_data_folder 2003 2016

python process.py your_data_folder

```

# If things go well:
## download.sh result:
![Alt](https://cloud.githubusercontent.com/assets/6142514/18031390/e8db55b6-6ca3-11e6-9094-25ee605f05d9.PNG)

## pocess.py result:
![Alt](https://cloud.githubusercontent.com/assets/6142514/18031405/74f7d8e4-6ca4-11e6-9a45-905b9fdb5791.PNG)

## Check out the example csv file
The data is in format

     
     | Currency pairs | time_stamp | Bid | Ask |
     | -------------- | ---------- | --- | --- |

&copy; 
[hptran.me](http://hptran.me)
