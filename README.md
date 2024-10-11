# Assignment 2: Text Extraction and Client-Facing Application

This project is designed to automate text extraction from PDF files using Airflow pipelines and create a client-facing application with FastAPI and Streamlit. The extracted data is stored in cloud storage (AWS S3), and users can interact with the extracted text through a user-friendly interface.

## Codelabs Link:

[Codelabs Link](https://codelabs-preview.appspot.com/?file_id=1-5QP7m-QK3vR2Jtv8-lNfvdp06IYvoHcKmNlVWzhRqU)

## Link for Video Submission: 

[Video Submission](https://your-video-submission-link)

## Link to Working Project:

[Deployment link](https://your-deployment-link)

## GitHub Project Link:

[GitHub Link](https://your-github-link)

---

## Project Structure

This repository contains the following directories and files:

```bash
Assignment2
├── .env
├── Architecture
│   ├── Architecture_Diagram.ipynb
│   ├── complex_architecture_diagram_with_openai.png
│   └── additional_images.png
├── AWS_S3
├── FastAPI
│   ├── app.py
│   ├── Dockerfile
│   └── pyproject.toml
├── LICENSE.md
├── Streamlit
│   ├── .env
│   ├── dockerfile
│   ├── app.py
│   ├── tree.txt
│   ├── requirements.txt
│   └── setup.sh
├── data.py
├── airflow_pipelines.py
├── LoadToS3.py
├── LoadToDatabase.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Project Files Description

### Root Directory
- **`.env`**: Contains environment variables for AWS, database, and OpenAI API connections.
- **`LoadToDatabase.py`**: Script to load extracted text into a database (e.g., PostgreSQL).
- **`LoadToS3.py`**: Script to upload extracted text files to AWS S3.
- **`airflow_pipelines.py`**: Airflow pipeline for automated text extraction.

### Streamlit Directory
This is the main directory for the Streamlit app and its components.

- **`app.py`**: The main entry point for the Streamlit application.
- **`dockerfile`**: Dockerfile for containerizing the Streamlit app.
- **`requirements.txt`**: Dependencies required to run the app.
- **`setup.sh`**: Setup script to configure the Streamlit environment.

---

### FastAPI Directory
Contains the FastAPI backend components.

- **`app.py`**: Entry point for FastAPI, handling user authentication and backend logic.
- **`Dockerfile`**: Dockerfile for containerizing the FastAPI app.
- **`pyproject.toml`**: FastAPI project configuration file for Poetry.

---

### Architecture Directory
Contains architecture-related files, including diagrams and Jupyter notebooks.

- **`Architecture_Diagram.ipynb`**: Jupyter notebook with architecture diagrams.
- **`complex_architecture_diagram_with_openai.png`**: PNG image of the detailed architecture diagram.
- **`additional_images.png`**: Placeholder for additional architectural diagrams.

---

## How to Run the Application

### Prerequisites and Setup Installation

1. Install **Poetry** for dependency management.
2. Ensure you have a `.env` file with the following environment variables:

```bash
AWS_ACCESS_KEY_ID=<your-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
POSTGRES_HOST=<your-rds-host>
POSTGRES_DB=<your-database>
POSTGRES_USER=<your-username>
POSTGRES_PASSWORD=<your-password>
OPENAI_API_KEY=<your-openai-api-key>

```
### Setup and Installation

The following are the commands to clone a repository from GitHub:

1. **Navigate to your desired directory** in the terminal (optional):
   ```bash
   cd /path/to/your/directory
   ```

2. **Clone the repository** using the `git clone` command followed by the repository URL:
   ```bash
   git clone https://github.com/username/repository-name.git
   ```

Replace `username` with the GitHub username and `repository-name` with the name of the repository you want to clone.

3. **Navigate to the cloned repository**:
   ```bash
   cd repository-name
   ```

This will clone the repository into the current directory and create a folder with the repository's name.

2. **Install dependencies**:

```bash
poetry install
```

3. **Run the Streamlit App**:

```bash
streamlit run Streamlit/app.py
```

4. **Run the Backend (FastAPI)**:

```bash
uvicorn FastAPI.app:app --reload
```

# How to Run the Codelabs File Locally

Once you have downloaded the cloned code, including the `assignment2-codelab` folder, follow these instructions to run it on your local machine.

## Prerequisites
Before running the Codelabs file, ensure the following tools are installed on your system:

- **Node.js** (needed for running a local web server) - [Download Link](https://nodejs.org/en/)
- **Git** (Optional, but useful for version control) - [Download Link](https://git-scm.com/)
- **Visual Studio Code (VS Code)** - [Download Link](https://code.visualstudio.com/)

## Step-by-Step Instructions

### Step 1: Install Node.js
If you haven't already, download and install **Node.js** from [here](https://nodejs.org/en/).

Verify that Node.js is installed correctly by running the following command in the terminal:

```bash
node -v
```
## Step-by-Step Instructions

### Step 1: Install Node.js
If you haven't already, download and install **Node.js** from [here](https://nodejs.org/en/).

Verify that Node.js is installed correctly by running the following command in the terminal:

```bash
node -v
```

### Step 2: Clone the Repository
If you haven't cloned the project repository, do so with the following steps:

1. Open a terminal window.
2. Use Git to clone the repository by running:

   ```bash
   git clone <your-repo-url>
   ```

3. Navigate to the folder containing the repository:

   ```bash
   cd <repository-folder>
   ```

### Step 3: Navigate to the `assignment2-codelab` Directory

1. Open **VS Code** and use the terminal to navigate to the `assignment2-codelab` directory, where the Codelab files are located:

   ```bash
   cd path_to_your_cloned_repo/Automated\ Text\ Extraction/assignment2-codelab
   ```

   Replace `path_to_your_cloned_repo` with the correct path to your cloned repository.

### Step 4: Install `http-server`

If you don't have the **http-server** package installed globally on your system, install it now using **npm**:

```bash
npm install -g http-server
```

### Step 5: Run the Codelab Locally

1. Start the local web server using **http-server** in the terminal:

    ```bash
    http-server
    ```

2. The terminal will show the URL where the server is running, such as:

    ```bash
    Starting up http-server, serving ./
    Available on:
      http://127.0.0.1:8080
    ```

3. Open your browser and go to the URL (e.g., [http://127.0.0.1:8080](http://127.0.0.1:8080)) to view and interact with the Codelab.

### Step 6: Troubleshooting

- If port **8080** is already in use or if there are any errors, you can start the server on a different port by running:

    ```bash
    http-server -p 8081
    ```

- Then, open the new URL in your browser (e.g., [http://127.0.0.1:8081](http://127.0.0.1:8081)).

### Step 7: View and Edit the Codelab

1. Open **VS Code** to view the files.
2. To make edits, modify the `index.html` or `codelab.json` files directly.
3. After editing, refresh the browser page where the Codelab is being served to view the changes.

## Contribution

- Saurabh Vyawahare - 33%
- Aniket Patole - 33%
- Shreya Bage - 33%

## Usage

1. **Login/Register**: Use the Streamlit interface to register a new user or log in.
2. **Upload PDFs**: After logging in, upload a PDF for text extraction via the Streamlit interface.
3. **Query Text**: Interact with the extracted text and query it using the OpenAI GPT model for further processing.
4. **View Results**: Review results and validate them through the user interface.

## Contributing

1. Fork the project.
2. Create a feature branch.
3. Submit a pull request for review.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.