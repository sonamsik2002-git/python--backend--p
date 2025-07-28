# papers/fetcher.py

import requests
import xml.etree.ElementTree as ET
import csv


def fetch_pubmed_ids(query, max_results=10):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_pubmed_details(pubmed_ids):
    ids = ",".join(pubmed_ids)
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.text


def parse_and_filter(xml_data):
    root = ET.fromstring(xml_data)
    results = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year")
        authors = []
        affiliations = []

        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName")
            fore_name = author.findtext("ForeName")
            affil = author.findtext(".//AffiliationInfo/Affiliation")

            if affil:
                affil_lower = affil.lower()
                if any(word in affil_lower for word in ["pharma", "biotech", "inc", "ltd", "corp", "gmbh"]):
                    authors.append(f"{fore_name} {last_name}")
                    affiliations.append(affil)

        if authors:
            results.append({
                "PubMedID": pmid,
                "Title": title,
                "PublicationDate": pub_date,
                "NonAcademicAuthors": "; ".join(authors),
                "CompanyAffiliations": "; ".join(affiliations)
            })
    return results


def save_to_csv(results, filename="results.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
