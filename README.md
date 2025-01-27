# Demo in drive

`https://drive.google.com/drive/folders/1Cv9PckHmCjDsLdWoL9Tr-UvHvclhiK9I?usp=drive_link`

## Video Demos

Here are two video demos to help you get started:

- [Instruction Video 1](Instructionvid/1.mov)
- [Instruction Video 2](Instructionvid/2.mov)
  
# Repo Analyzer

This project provides tools for cloning GitHub repositories and analyzing their complexity. It includes functionalities for extracting complex functions and creating prompts for AI-based analysis.

## Files

- **clone_repo.py**: Contains functions to clone repositories, analyze complexity, extract complex functions, and manage cleanup operations.

## Key Functions

- `clone_repository(repo_url, save_path="cloned_repos")`: Clones a GitHub repository to a specified directory.
- `analyze_complexity(repo_path, analysis_path="analysis")`: Analyzes cyclomatic complexity in Python files.
- `extract_complex_functions(repo_path, analysis_path="analysis")`: Extracts functions or classes with high complexity.
- `create_final_prompt_for_composer(repo_path, analysis_path="analysis")`: Creates a final prompt for Cursor AI Composer.
- `cleanup(repo_path, analysis_path="analysis")`: Deletes the cloned repository and its analysis.
- `clean_analysis_files(analysis_path="analysis")`: Cleans up analysis files without removing the cloned repository.

## Usage

Run the `main()` function in `clone_repo.py` to access the command-line interface for these functionalities. Follow the prompts to clone repositories, analyze complexity, and manage files.

## Requirements

- Python 3.x
- GitPython
- Radon

Ensure these dependencies are installed before running the script. You can install them using pip:

```bash
pip install gitpython radon
```

## Step-by-Step Instructions

1. **Clone a Repository**:
   - Run the script and enter the GitHub repository URL when prompted.
   - Example: `https://github.com/user/repo.git`

2. **Run Complexity Analysis**:
   - Choose option 1 from the menu to analyze cyclomatic complexity.
   - The results will be saved in `analysis/complexity.txt`.

3. **Extract Complex Functions**:
   - Choose option 2 to extract functions or classes with high complexity.
   - The extracted context will be saved in `analysis/extracted_context.txt`.

4. **Create Final Prompt for AI**:
   - Choose option 3 to generate a final prompt for AI analysis.
   - The prompt will be saved in `final_prompt.md`.

5. **Clean Up Files**:
   - Choose option 4 to clean up analysis files without removing the cloned repository.
   - Choose option 5 to delete the cloned repository and all analysis files.

6. **Copy Final Prompt to Cursor AI Composer**:
   - Choose option 6 to display the final prompt for copying into Cursor AI Composer.

7. **Exit**:
   - Choose option 7 to exit the program.


## Example Commands

- To install dependencies:
  ```bash
  pip install gitpython radon
  ```

- To run the script:
  ```bash
  python clone_repo.py
  ```

## Troubleshooting

- **Invalid URL**: Ensure the URL starts with `http` and points to a valid GitHub repository.
- **Missing Dependencies**: Install the required packages using pip.
- **File Not Found**: Ensure the analysis files are generated before attempting to access them. 
