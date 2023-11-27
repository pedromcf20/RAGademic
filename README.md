# RAGademic: Retrieval-Augmented Generation (RAG) Tool for Academic Research

This project presents a specialized tool for extracting and analyzing academic papers from the arXiv preprint repository. Utilizing the Retrieval-Augmented Generation approach, it assists researchers in streamlining their literature review process by automating the download, parsing, and questioning of relevant papers.

## Features

- **Automated Retrieval:** Downloads papers based on user-defined arXiv search queries.
- **Data Chunking:** Breaks down papers into manageable chunks for processing.
- **Embedding Generation:** Converts text chunks into embeddings using OpenAI's API.
- **Chroma Vector Database:** Stores and manages embeddings for efficient retrieval.
- **Question-Answering System:** Leverages a GPT-3.5 Turbo model for informed responses.
- **Source Referencing:** Provides answers with references to the original academic papers.

## Installation

Ensure you have Python installed on your system. This tool has been tested with Python 3.11.

1. **Clone the Repository:**
```sh
   git clone https://github.com/pedromcf20/RAGademic.git
   cd rag-tool
```

2. **Install Dependencies:**
Before running the application, install the necessary Python libraries listed in requirements.txt.
```sh
    pip install -r requirements.txt
```

3. **Set Up the .env File:**
Create a .env file in the root directory of the project and add your OpenAI API key.
```env
    OPENAI_API_KEY=your-api-key-here
```

## Usage

To run the tool, navigate to the project directory and execute the main script.

1. **Load Environment Variables:**
Make sure the .env file is set up with your OpenAI API key.

2. **Run the Tool:**
```sh
    python src/run_ragademic.py
```
Follow the on-screen prompts to input your arXiv search query and question.

## Configuration
<ul>
<li>The tool is pre-configured to work with the arXiv repository and OpenAI's GPT-3.5 Turbo model.</li>
<li>Adjustments can be made in the script for different data sources or models, based on user requirements.</li>
</ul>


## Contributions
Contributions to this project are welcome. 
Please submit a pull request or raise an issue for bugs, feature requests, or enhancements.

## License
This project is licensed under the MIT Licens