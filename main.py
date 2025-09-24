from typer import Typer
import os
from utils import dataget, xmlparser, TEXT, DATA
from typing import Optional


URL = "https://spraakbanken.gu.se/lb/resurser/meningsmangder/"

for directory in [DATA, TEXT]:
    if not os.path.exists(directory):
        os.mkdir(directory)

app = Typer()


@app.command()
def get_data(n_cores: Optional[int] = None):
    """
    Gets data by downloading from specified URL to a local directory.

    This command uses the dataget class to fetch links and download data.

    Args:
        n_cores: Optional[int]
            Number of CPU cores to use for parallel downloading.
            If None, all available cores minus 4 will be used.

    Example:
        $ python main.py get-data
        $ python main.py get-data --n-cores 4
"""
    datagetter = dataget(URL, DATA, n_cores)
    datagetter.get_links()
    datagetter.download()

@app.command()
def process_data(n_cores: Optional[int] = None):
    """
    Process XML data files by decade using parallel processing.
    
    This function initializes an XML parser and processes data for each decade.
    It combines temporary files into a single text file for each decade and 
    removes the temporary files afterward. If a decade's file already exists,
    it skips processing for that decade.
    
    Args:
        n_cores (Optional[int]): Number of CPU cores to use for parallel processing.
            If None, all available cores minus 4 will be used.
    
    Returns:
        None
    
    Side effects:
        - Creates decade directories under TEXT directory if they don't exist
        - Combines temporary files into a single decade file
        - Deletes temporary files after processing
        - Prints status messages about skipped decades
    """
    xmlparserr = xmlparser(DATA, TEXT, n_cores)
    for decade in xmlparserr.decades:
        xmlparserr.process_decade(decade)
        if not os.path.exists(f"{TEXT}/{decade}/{decade}.txt"):
            os.makedirs(f"{TEXT}/{decade}", exist_ok=True)
            tmps = [f for f in os.listdir(f"{TEXT}/{decade}") if f.endswith(".tmp")]
            with open(f"{TEXT}/{decade}/{decade}.txt", "w") as f:
                for tmp in tmps:
                    with open(f"{TEXT}/{decade}/{tmp}") as tmp_f:
                        f.writelines(tmp_f.readlines())
                    os.remove(f"{TEXT}/{decade}/{tmp}")
        else:
            print(f"{decade} already processed, skipping.")

if __name__ == "__main__":
    app()