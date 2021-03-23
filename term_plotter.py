import os, json
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import argparse

sns.set(style="whitegrid")

# Register matplotlib converters as required by future versions of pandas
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def generate_df(terms, path='./us_presidential_speeches/', title=None, output=None, default_output=None):
    # Initialize dictionary df which will be converted into pandas DataFrame later
    df = {
        'Date': [],
        'Term': [],
        'Score': []
    }


    dates = []
    contents =[]

    # Capture invalid paths
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print('Invalid path.')
        return None
        
    # Read in speech files, extract dates and speech contents
    for file in files:
        with open(path+file,'r') as infile:
            speech = json.load(infile)
            # Convert date format
            speech_date = datetime.strptime(speech['Date'],  '%B %d, %Y').strftime('%Y-%m-%d')
            speech_content = speech['Speech']
            dates.append(speech_date)
            contents.append(speech_content)

    # Create list of stop words to remove
    stop_words = list(stopwords.words('english'))

    # Fit TfidfVectorizer on list of speech contnts
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3),
                                   stop_words=stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform(contents)
    tfidf_matrix = np.asarray(tfidf_matrix.todense())

    # Retrieve words as features
    features = list(tfidf_vectorizer.get_feature_names())
    
    # Turn all words in speech contents into lowercase
    contents = [content.lower() for content in contents]

    # Capture term(s) not in speech vocabulary
    idx = []
    match = []
    no_match = []
    for term in terms:
        try:
            idx.append(features.index(term))
            match.append(term)
        except ValueError:
            no_match.append(term)

    # Print error message
    if len(no_match) != 0:
        for term in no_match:
            print(term, 'is not in speech dictionary')

    # Construct DataFrame
    if len(idx) != 0:
        for i in range(len(idx)):
            for j in range(tfidf_matrix.shape[0]):
                df['Date'].append(dates[j])
                df['Term'].append(match[i])
                if match[i] in contents[j]:
                    df['Score'].append(tfidf_matrix[j, idx[i]])
                else:
                    df['Score'].append(0)

        df = pd.DataFrame(df)
        df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
        df = df.sort_values(by='Date')
        
        # Plot the graph
        graph = sns.lineplot(x="Date", y="Score", hue="Term", data=df)
        
        # Set graph title
        if title != None:
            graph.set_title(title)

        # Set graph output name
        fig = graph.get_figure()
        if output!= None:
            fig.savefig(output)
        else:
            fig.savefig(default_output)
            
    # Capture case where all terms are not in speech dictionary
    else:
        print('No term input is in speech dictionary, and therefore no graph can be plotted.')


# Create a parser
parser = argparse.ArgumentParser(description='Plot tf-idf scores of different terms over time')

# Add an argument for terms (strings in quotations separated by spaces)
parser.add_argument('--terms', help='Input term strings', nargs='+')

# Add an optional argument for path
parser.add_argument('--path', help='Input the speech directory', nargs='?', default='./us_presidential_speeches/')

# Add an optional argument for graph title
parser.add_argument('--title', help='Input the graph title', nargs='?', default=None)

# Add an optional argument for output name
parser.add_argument('--output', help='Input the output name', nargs='?', default=None)

# Parse command argument
args = parser.parse_args()

# Get terms
terms = []
for arg in args.terms:
    terms.append(arg.lower())

# Generate default output name
default_output = ''
for term in terms:
    default_output = default_output + '_' + term
default_output = default_output[1:]
    
# Get path
if args.path != None:
    path = []
    for c in args.path:
        path.append(c)
    path = ''.join(path)

# Get title
if args.title != None:
    title = []
    for c in args.title:
        title.append(c)
    title = ''.join(title)
else:
    title = None

# Get output
if args.output != None:
    output = []
    for c in args.output:
        output.append(c)
    output = ''.join(output)
else:
    output = None


df = generate_df(terms=terms, path=path, title=title, output=output, default_output=default_output)

