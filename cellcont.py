import pandas as pd
import wikipedia as wp

# Get the html source
html = wp.page("List of contaminated cell lines").html().encode("UTF-8")
df = pd.read_html(html)[0]
df.to_csv('beautifulsoup_pandas.csv', header=0, index=False)
print(df)
 
