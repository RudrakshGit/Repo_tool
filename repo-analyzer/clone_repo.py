import os
import subprocess
import shutil
from git import Repo
import time


def clone_repository(repo_url, save_path="cloned_repos"):
    """Clones a GitHub repository to a specified directory."""
    print("Cloning the repository. Please wait...")
    start_time = time.time()
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(save_path, repo_name)
    try:
        Repo.clone_from(repo_url, repo_path)
        elapsed_time = time.time() - start_time
        print(f"Repository cloned to {repo_path} in {elapsed_time:.2f} seconds.")
        return repo_path
    except (OSError, subprocess.SubprocessError) as e:
        print(f"Error cloning repository: {e}")
        return None


def analyze_complexity(repo_path, analysis_path="analysis"):
    """Analyzes cyclomatic complexity in Python files."""
    print("Starting complexity analysis. Please wait...")

    if not os.path.exists(analysis_path):
        os.makedirs(analysis_path)

    complexity_file = os.path.join(analysis_path, "complexity.txt")
    high_complexity_count = 0

    with open(complexity_file, "w") as output:
        output.write(f"Cyclomatic Complexity Analysis for {repo_path}:\n\n")

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    print(f"Analyzing: {file_path}")
                    try:
                        result = subprocess.run(
                            ["python3", "-m", "radon", "cc", "-s", "-a", file_path],
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        output.write(f"File: {file_path}\n")
                        output.write(result.stdout)
                        output.write("\n")

                        for line in result.stdout.splitlines():
                            if any(grade in line for grade in ["C (", "D (", "F ("]):
                                high_complexity_count += 1
                    except subprocess.CalledProcessError as e:
                        print(f"Error analyzing {file_path}: {e.stderr}")

    print(f"Complexity analysis saved to {complexity_file}")
    print(f"High-complexity functions/classes found: {high_complexity_count}")
    return high_complexity_count


def extract_complex_functions(repo_path, analysis_path="analysis"):
    """Extracts functions or classes with high complexity."""
    print("Extracting context for high-complexity functions/classes...")

    complexity_file = os.path.join(analysis_path, "complexity.txt")
    extraction_file = os.path.join(analysis_path, "extracted_context.txt")

    try:
        with open(complexity_file, "r") as input_file, open(extraction_file, "w") as output_file:
            output_file.write("Extracted High-Complexity Context:\n\n")
            current_file = ""
            for line in input_file:
                if line.startswith("File: "):
                    current_file = line.replace("File: cloned_repos/spaCy/", "").strip()
                    output_file.write(f"\n### File: {current_file} ###\n")
                elif any(grade in line for grade in ["C (", "D (", "F ("]):
                    output_file.write(f"Location: {current_file}\n")
                    output_file.write(line)
                    print(f"Extracted: {line.strip()} from {current_file}")

        print(f"Extracted context saved to {extraction_file}")
    except OSError as e:
        print(f"Error extracting complex functions: {e}")
        return None


def create_final_prompt_for_composer(repo_path, analysis_path="analysis"):
    """Creates a single final prompt for Cursor AI with simplified instructions."""
    print("Creating the final prompt for Cursor AI Composer...")

    try:
        # Define file paths using relative paths
        extracted_context_file = os.path.join(analysis_path, "extracted_context.txt")

        # Ensure necessary files exist
        if not os.path.exists(extracted_context_file):
            raise FileNotFoundError(f"Required file not found: {extracted_context_file}")

        # Write the final prompt
        final_prompt_path = "final_prompt.md"
        with open(final_prompt_path, "w") as output:
            output.write(
                f"Read the following files:`extracted_context.txt`,`repo-analyzer/cloned_repos/{os.path.basename(repo_path)}`."
                f"I have cloned a repository located at `repo-analyzer/cloned_repos/{os.path.basename(repo_path)}`. \n"
                f"The extracted high-complexity context is in `extracted_context.txt`. "
                f"Please read all the files in the repository and the `extracted_context.txt` file. "
                f"Generate meaningful, complex, and challenging multiple-choice questions (MCQs) based on the codebase.\n"
                f"The questions should be diverse and not focused on specific areas, covering the codebase broadly. "
                f"All questions should be multiple-choice with four options, and both the questions and options should be very difficult to solve. "
                f"Use clickable file paths in the questions to allow easy navigation to the files.\n"
                f"Avoid simplistic or obvious questions. Make them insightful, thought-provoking, and based on multiple files wherever possible."
            )

        print(f"Final prompt saved to {final_prompt_path}")
        return final_prompt_path

    except (OSError, FileNotFoundError) as e:
        print(f"Error creating final prompt: {e}")
        return None



def cleanup(repo_path, analysis_path="analysis"):
    """Deletes the cloned repository and its analysis."""
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            print(f"Deleted cloned repository: {repo_path}")
        if os.path.exists(analysis_path):
            shutil.rmtree(analysis_path)
            print(f"Deleted analysis directory: {analysis_path}")
    except OSError as e:
        print(f"Error during cleanup: {e}")


def clean_analysis_files(analysis_path="analysis"):
    """Cleans up analysis files without removing the cloned repository."""
    try:
        if os.path.exists(analysis_path):
            for file in ["complexity.txt", "extracted_context.txt"]:
                file_path = os.path.join(analysis_path, file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            print("Analysis files cleaned successfully.")
        if os.path.exists("final_prompt.md"):
            os.remove("final_prompt.md")
            print("Final prompt file cleaned.")
    except OSError as e:
        print(f"Error cleaning analysis files: {e}")


def main():
    repo_url = input("Enter GitHub repository URL: ").strip()
    if not repo_url.startswith("http"):
        print("Invalid URL. Please enter a valid GitHub repository URL.")
        return
    
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("cloned_repos", repo_name)
    
    if not os.path.exists(repo_path):
        repo_path = clone_repository(repo_url)
        if not repo_path:
            print("Failed to clone repository. Exiting...")
            return

    while True:
        print("\nWhat would you like to do?")
        print("1. Run complexity analysis")
        print("2. Extract complex functions")
        print("3. Create final prompt for Cursor AI")
        print("4. Clean up analysis files")
        print("5. Clear the cloned repository and exit")
        print("6. Copy the final prompt to the Cursor AI Composer")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            high_complexity_count = analyze_complexity(repo_path)
            print("Step 1: Complexity analysis completed.")
        elif choice == "2":
            extract_complex_functions(repo_path)
            print("Step 2: Extracted high-complexity functions.")
        elif choice == "3":
            final_prompt_file = create_final_prompt_for_composer(repo_path, analysis_path="analysis")
            if final_prompt_file:
                print(f"Step 3: Final prompt created. Copy the contents of {final_prompt_file} and paste it into Cursor AI.")
        elif choice == "4":
            clean_analysis_files()
            print("Step 4: Analysis files cleaned.")
        elif choice == "5":
            cleanup_choice = input("Do you want to clean up the cloned repository? (yes/no): ").strip().lower()
            if cleanup_choice == "yes":
                cleanup(repo_path)
            print("Step 5: Cloned repository and analysis cleaned. Exiting...")
            break
        elif choice == "6":
            try:
                with open("final_prompt.md", "r") as f:
                    final_prompt = f.read()
                    print("\nCopy the final prompt below and paste it into the Cursor AI Composer:")
                    print("-" * 50)
                    print(final_prompt)
                    print("-" * 50)
            except FileNotFoundError:
                print("Error: Final prompt file not found. Please generate it first.")
        elif choice == "7":
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
