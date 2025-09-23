from tqdm import tqdm 
import requests
from bs4 import BeautifulSoup
import os
import multiprocessing
from multiprocessing import Pool
from loguru import logger
import xml.etree.ElementTree as ET 

TEXT = "test/"
DATA = "data/"

class dataget:
    def __init__(self, URL, DATA, N_CORES):
        self.URL = URL
        self.DATA = DATA
        if N_CORES is None:
            self.N_CORES = multiprocessing.cpu_count() - 4
        else:
            self.N_CORES = N_CORES
        logger.info(f"Using {self.N_CORES} threads")
        self.URL = URL

    def get_links(self):
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a")
        to_dl = [self.URL + link.text for link in links if "kubhist2" in link.text]
        self.missing = [link for link in to_dl if not os.path.exists(f"data/{link.split('/')[-1].replace('.bz2', '')}")]
        logger.info(f"There are {len(to_dl)} files in total, and {len(self.missing)} missing.")

    def download_and_extract(self, link):
        r = requests.get(link, allow_redirects=True)
        with open(f"data/{link.split('/')[-1]}", "wb") as f:
            f.write(r.content)
        logger.info(f"{link}: downloaded, decompressing")
        os.system(f"bzip2 -d data/{link.split('/')[-1]}")
        logger.info(f"{link}: decompressed")
        return

    def download(self):
        with Pool(processes=self.N_CORES) as pool:
            r = list(tqdm(pool.imap(self.download_and_extract, self.missing), total=len(self.missing)))
        del r
        return
    
class xmlparser:
    def __init__(self, DATA, TEXT, N_CORES = None):
        self.DATA = DATA
        self.TEXT = TEXT
        if N_CORES is None:
            self.N_CORES = multiprocessing.cpu_count() - 4
        else:
            self.N_CORES = N_CORES
        logger.info(f"Using {self.N_CORES} threads")
        self.xmls = [f for f in os.listdir(DATA) if f.endswith(".xml")]
        self.decades = [f.split("-")[-1].split(".")[0] for f in self.xmls]
        self.decades = list(set(self.decades))
        self.decades.sort()
        logger.info(f"There are {len(self.xmls)} xml files in total, spanning {len(self.decades)} decades.")

    def process_decade(self, decade):
        if not os.path.exists(self.TEXT+decade+"/"+f"{decade}.txt"):
            files = [xml for xml in self.xmls if decade in xml]
            logger.info(f"{decade}: {len(files)} to parse")

            with Pool(self.N_CORES) as p:
                r = list(tqdm(p.imap(extract_sentences, files), total=len(files)))
            del r

def _words_to_file(sentence_dict, file, decade):
    if not os.path.exists(TEXT+decade):
        os.mkdir(TEXT+decade)
    with open(TEXT+decade+"/"+file, "a") as f:
        for v in sentence_dict.values():
            if len(v) > 4:
                try:
                    merged = v[:-2] + [''.join(v[-2:])]
                    s_out = " ".join(merged) + "\n"
                    f.write(s_out)
                except ValueError:
                    continue
        
    return

def extract_sentences(file):
        tmp_out = file.replace(".xml", ".tmp")
        xml_iter  = ET.iterparse(DATA+file, events=('start','end'))
        decade = file.split("-")[-1].split(".")[0]

        sentence_dict = {}
        counter = 0
        for event, y in xml_iter:
            
            if y.tag == 'sentence' and event == "start":
                counter += 1
                sentence_list = []
                for z in y.findall(".//token"):
                    sentence_list.append(z.text)
                sentence_dict[counter] = sentence_list

                if counter % 100000 == 0:
                    _words_to_file(sentence_dict, tmp_out, decade)
                    sentence_dict = {}
                
            y.attrib.clear()
            y.text = None
            y.clear()

        _words_to_file(sentence_dict, tmp_out, decade)           
        
        return