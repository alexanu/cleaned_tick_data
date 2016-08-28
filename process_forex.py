# coding: utf-8
import glob
import os
import zipfile
import pandas as pd
import numpy as np
import optparse
import time
import re
import shutil
from dateutil.parser import parse
DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f"


def unzip_and_clean(cname, inpath, outpath=None):
    """ 
     Unzip file from folder and only take the file in format
     |Currency pairs|time_stamp|Bid|Ask 
     without column header
    If no outpath is specified, file uncompress to 'unzip' folder that is sibling to directory containing the zip files
    """
    
    search = re.search(r'[0-9]+(.*)(?=.zip)', inpath) # take the name of zip file to rename new csv file
    file_name = search.group() + '.csv'
    
    search = re.search(r'(.*)(?={})'.format(search.group()), inpath ) 
    dir_parent = search.group() # parent directory
    
    if outpath:
        dir_parent = outpath
        
    dir_unzip = os.path.join(dir_parent, "unzip")
    dir_outpath = os.path.join(dir_parent, "clean_output")
    
    if not os.path.exists( dir_unzip ):    
        os.mkdir(dir_unzip) # Now create tmp unzip folder
    
    
    if not os.path.exists( dir_outpath ):
        os.mkdir(dir_outpath)
    
    files = None
    df = None
    
    try:
        # UNzip file
        with zipfile.ZipFile(inpath) as f:
            f.extractall(dir_unzip)
            unzip_file = glob.glob(os.path.join(dir_unzip,"{}*.csv".format(cname)))
            
    except (FileNotFoundError):
        print ("/nOnly accept inpath to .zip file")
    
    files = unzip_file[0] if unzip_file else None
    # read data into data frame
    # Gain Capital has some legacy issue with encoding, there are maybe few more encoding out there
    try:
        try:
            df = pd.read_csv(files, error_bad_lines=False, header=None, encoding='utf-8', skiprows=1)
        except: 
            df = pd.read_csv(files, error_bad_lines=False, header=None, encoding='utf-16', skiprows=1)
    except:
        print ("ERROR: {} is bad. Skip reading".format(files))
        return None # skip bad file
    
    df = df.dropna()
    
    # Put everything in format
    # -----------------------------------
    # |Currency pairs|time_stamp|Bid|Ask|
    # -----------------------------------

    nrows, ncols = df.shape
    cols_names = {} # store column index to extract later, some file is not in persistent order
    
    for i in range(ncols):
        val = df.iat[0,i]

        if val == re.sub(r'[^a-zA-Z0-9]','/',cname):
            # Some files is miszip, just ignore them
            cols_names['Pairs'] = i
            continue
        
        try:
            parse(val)
            cols_names['TimeStamp'] = i
            break # We always assume column next to timestamp column is bid, then ask
        except (ValueError, AttributeError):
            pass

    cols_names['Bid'] = i+1
    cols_names['Ask'] = i+2
    
    try:
        clean_df = df.iloc[ : , [cols_names['Pairs'], cols_names['TimeStamp'], cols_names['Bid'], cols_names['Ask']]]
    except:
        # currency pair that is save incorrectly to the zip file
        return None
    
    clean_df.columns = ['Pairs','TimeStamp', 'Bid', 'Ask']
    clean_df.sort_values(by='TimeStamp') # prevent unorder tick
    
    writepath = os.path.join(dir_outpath, file_name)
    if not os.path.exists(writepath):
        clean_df.to_csv(path_or_buf=writepath, encoding='utf-8', index=False, header=False, date_format=DATEFORMAT)
        print("Save {} to location {}".format(file_name, dir_outpath))
    else:
        print("File already exist at: {}".format(writepath))
    
    shutil.rmtree(dir_unzip) # Clean the unzip folder
    
    print("-"*40,"\n")
    
    
    
def process(dir_path):
    """
    Read the zip files download from Gain Capital, unzip, extract to new csv files
    in format | Currency pair | TimeStamp | Bid | Ask |. 
    Files are save in folder called clean_output
    
    Args: 
        dir_path: path to directory that contains currency pair folder
    
    """
    cpairs = os.listdir(dir_path)
    for pair in cpairs:
        zipath = os.path.join(dir_path,pair)
        zipfiles = os.listdir(os.path.join(zipath,"tmp_folder"))
        for f in zipfiles:
            inpath = os.path.join(zipath,"tmp_folder",f)
            print ("Processing.... ",inpath)
            unzip_and_clean(pair, inpath,zipath)
        print("\tDONE Processing {}".format(pair))
        print("<{}>".format("="*40))

    
    
if __name__ == "__main__":
    version = "1.0"
    usage = "%prog -i <input path>"
    parser = optparse.OptionParser(usage, None, optparse.Option, version)
    
    parser.add_option('-i',
                      '--input',
                       dest='inpath',
                       help='Input file')
    
    (options, args) = parser.parse_args()
    
    process(options.inpath)

   
