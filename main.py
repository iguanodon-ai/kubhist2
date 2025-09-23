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
    datagetter = dataget(URL, DATA, n_cores)
    datagetter.get_links()
    datagetter.download()

@app.command()
def process_data(n_cores: Optional[int] = None):
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