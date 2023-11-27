import logging
import os
from typing import List

import arxiv


def fetch_arxiv_papers(search_query: str, max_results: int = 3, download_dir: str = 'arxiv_papers') -> List[str]:
    """
    Fetches papers from arXiv based on a search query and downloads them.

    Args:
    search_query (str): The search query to find papers on arXiv.
    max_results (int): Maximum number of papers to download. Default is 10.
    download_dir (str): Directory where the downloaded papers will be saved.

    Returns:
    List[str]: List of downloaded file paths.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        logging.info(f"Created directory {download_dir} for downloading papers.")

        # Initialize the arXiv client
        client = arxiv.Client()
        logging.info("Initialized arXiv client.")

        # Initialize the search
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        logging.info(f"Searching arXiv for papers related to: '{search_query}'.")


        downloaded_files = []
        for paper in client.results(search):
            try:
                # Download the paper
                filename = paper.download_pdf(dirpath=download_dir)
                downloaded_files.append(filename)
                logging.info(f'Downloaded {filename}')
            except Exception as e:
                logging.error(f'Error downloading {paper.title}: {e}')

        return downloaded_files
      
    except Exception as e:
        logging.error(f'Error in fetch_arxiv_papers: {e}')
        return []