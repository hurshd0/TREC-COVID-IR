# TREC-COVID 2020 Task - Building simple yet effective pandemic retrieval engine
---

TREC-COVID Challenge is an Information Retrieval (IR) challenge sponsored by NIST in colaboration with Allen Institute for AI and other industry leading research groups. I used Round 3 dataset which contains 40 topics, where each topic represent user's infomation need. The goal of challenge is to retrieve relevant documents for each topic, and evalute them against human judgements. 

## Method

I tried TF-IDF based approach raning from builting one from scratch using Python, and comparing it with two famous open-source commercial search engine - Solr and Elasticsearch. To improve rankins I also tried Automated Query Expansion using Word Embeddings and Deep learning based Re-ranking technique. 

## In this repo

- `scripts` - contains bash scripts to download dataset, and install trec eval tool
- `notebooks` - contains documentation, trec-eval results, and notes on results
