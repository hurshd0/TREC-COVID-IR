from pathlib import Path
import json
import time
import os
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import tensorflow as tf
import tensorflow_hub as hub

class ESIndex:
    
    def __init__(self, index_name: str, index_settings_fpath: str):
        self.index_name = index_name
        self.index_settings_fpath = Path(index_settings_fpath)
        if not self.index_settings_fpath.exists():
            raise FileNotFoundError(f"Path specified doesn't exist, check again: {index_settings_fpath}")
        self.settings = self._load_index_settings(self.index_settings_fpath)
    
    def 
    
    
    
    def _load_index_settings(self, fpath: Path):
        with open(fpath, encoding='utf-8') as reader:
            source = reader.read().strip()
        return source
        

