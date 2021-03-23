# Diachronic Term Relevance
The `term_plotter.py` program works with several libraries including `numpy`, `pandas`, `seaborn`, and `scikit-learn` to calculate the tf-idf scores of a set of specified terms as they occur in each of the scraped presidential speeches and plot each term’s score as a function of time (i.e. the speech’s date).

## Argument
The arguments taken by the program are:
- `terms`: a list of up to five terms in quotations, separated by white space. Each “term” can consist of three tokens (e.g a trigram), with English stopwords assumed
to be filtered out.
- `path`: an optional string argument that specifies where the speech directory is. If not provided, the program should assume to look at the folder in the current directory, e.g.: `./us_presidential_speeches`.
- `title`: an optional string argument that adds a title to the plot. If not provided, the program outputs the plot without a title.
- `output`: an optional string argument that saves the plot under the specified name. If not provided, saves the plot as the concatenation of all terms, separated by an underscore token. e.g.: `america_united_states.png`.

## Densign
This program defines one function `generate_df` and uses the library `argparse` to interact with the command-line interface.

### `generate_df`
The function first reads in speech files and stores speech contents and corresponding dates into a dictionary. During the file-read-in process, `FileNotFoundError` exception is checked, and when the path is invalid, an error message is printed and the program is ended. After reading in the files, the program then fits `TfidfVectorizer` on the contents and produces a matrix of which the (i,j) entry corresponds to the tf-idf score of j-th word in i-th speech.

Then for each term in the input argument `terms`, the tf-idf score and corresponding date are extracted from the matrix and populated into a `pandas.Dataframe`. During the extraction process, `ValueError` exception is checked to make sure that only term that exists in speech vocabulary will be populated into the `DataFrame` and for each non-existing term, an error message will be printed. Finally, the `DataFrame` object (if not empty) will be plotted using `seaborn`.

### `argparse`
The `argparse` library enables the initialization of a `parser` object and the addition of different arguments. In particular, by setting `nargs='?'`, the argument becomes optional.

The parsed arguments can then be concatenated and processed, and fed into the `generate_df` function.

## Usage
Call one or more arguments to the program script, where the first argument should be up to five strings (each can be either unigram, bigram, or trigram) in quotations, separated by white space. The second argument is a string of file path. The third argument is a string of intended title of the graph. The forth argument is a string of intened file name of the graph.

Below are examples of legal calls:

    % python3 term_plotter.py --terms "america" "united states"

or

    % python3 term_plotter.py --terms "america" "united states" \
                              --path "/Users/apple/Desktop/us_presidential_speeches"

or

    % python3 term_plotter.py --terms "america" "united states" \
                              --path "/Users/apple/Desktop/us_presidential_speeches"
                              --title "’America’ vs. ’United States’"

or

    % python3 term_plotter.py --terms "america" "united states" \
                              --path "/Users/apple/Desktop/us_presidential_speeches"
                              --title "’America’ vs. ’United States’"
                              --output "myplot"

etc.    








