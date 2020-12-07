import pysolr
from pathlib import Path
import pandas as pd

def create_solr_connection(collection_name, solr_connection_url):
    """Creates Solr connection
    """
    solr = pysolr.Solr(
        "{}/solr/{}".format(solr_connection_url, collection_name),
        always_commit=True,
        timeout=10
    )
    return solr

def get_ranked_lists(query: str, qid: int, run_name: str, solr: pysolr.Solr, top_k: int) -> list:
    """Get Top k ranked lists from Solr index"""
    solr_query = f"text:{query}"
    solr_query_param = {
        "fl": "id,score",
        "rows": top_k
    }
    template = "{} Q0 {} {} {:.6f} {}\n"
    results = solr.search(solr_query, **solr_query_param).docs
    return [template.format(qid, row['id'], idx+1, row['score'], run_name) for idx, row in enumerate(results)]

def write_results(output_fpath: Path, query_df: pd.DataFrame, query_txt_col: str, solr: pysolr.Solr, run_name: str, top_k=1000):
    """Writes retrieved resuls to text file"""
    with open(output_fpath, 'w', encoding='utf-8') as writer:
        for idx, query_row in query_df.iterrows():
            qid = idx
            query = query_row[query_txt_col]
            ranked_lists = get_ranked_lists(query, qid, run_name, solr, top_k)
            writer.writelines(ranked_lists)
