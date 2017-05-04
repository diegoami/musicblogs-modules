import argparse
import pandas as pd
import pickle
from datetime import datetime

datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

parser = argparse.ArgumentParser()

parser.add_argument('--inputfile')
parser.add_argument('--outputfile')
parser.add_argument('--debug')


args = parser.parse_args()
debug = False if args.debug == None else True


with open(args.inputfile, 'rb') as handle:
    videoMap = pickle.load(handle)
    print(videoMap)
    df = pd.DataFrame.from_dict(videoMap,orient='index')
    df.columns = ['title', 'videoId','lastOk']
    df.index.name = 'postId'
    print(df.info())
    df = df.sort(columns='lastOk', ascending=True)
    df.to_csv(args.ouputfile, encoding='utf-8')
