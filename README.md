# research-report-dataset
## Usage
1. Install the required package: PyMuPDF==1.20.2

2. Replace the value of the following variables in the **generate_content.py** with the correct paths:
     - **metadata**: the path to the metadata JSON file.
     - **dataset**: the path to the dataset JSON file.
     - **directory**: the path to the folder containing the research report PDF files.

3. To run the script, simply run the following command:
```bash
python generate_content.py
```

The script will create a new JSON file that merges the original dataset with the extracted text content from PDF files based on the start index and end index. The JSON file will be saved with a filename suffix of ***(with_content)*** added to the original filename.