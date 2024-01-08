# Project Gutenberg Book Analysis

## Overview

This project presents a detailed analysis of Project Gutenberg's extensive collection of books, highlighting its significance not just for literature enthusiasts but also for those delving into Natural Language Processing (NLP). By examining patterns in publication trends, author prolificacy, and book categorizations, we gain invaluable insights into the literary landscape. Project Gutenberg, a vital resource for freely available texts, is commonly used in various NLP applications and serves as a foundational dataset for those learning NLP with tools like the NLTK library.

## Data Extraction and Processing

We utilized the daily-updated RDF/XML metadata from Project Gutenberg to curate our dataset. With the aid of `rdflib` and `sparql`, we extracted pertinent details such as book titles, publication years, author names, and more. This information was meticulously compiled into a new, user-friendly CSV file format, enabling us to conduct our analyses with greater efficiency and clarity.

## Analysis Insights

Our analysis delved into diverse facets of the Project Gutenberg collection, uncovering the most published authors within the dataset and identifying books that boasted the highest number of contributors. We explored the genres and multiple categories these books were associated with, as well as the languages in which they were available. Notably, we charted the most downloaded texts, providing a unique glimpse into reader preferences, and highlighted the popularity of non-English texts. This comprehensive study not only contributes to our understanding of historical publication trends but also offers a rich corpus for ongoing and future NLP projects.