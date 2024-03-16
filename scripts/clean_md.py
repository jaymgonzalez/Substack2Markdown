import re
import os
import pathlib
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Regular expression to match Markdown image syntax
def remove_image_links(md_content):
    logging.info("Removing image links")
    # Regular expression to match Markdown image syntax
    img_pattern = r"\[?\!\[.*?\]\(.*?\)\]?"
    # Replace found patterns with empty string
    cleaned_content = re.sub(img_pattern, "", md_content)
    return cleaned_content


def remove_any_date_to_title(md_content):
    logging.info("Removing any date to title")
    # Regular expression to match any date in the format **MMM DD, YYYY**
    # followed by any content, non-greedy, until "## Ahoy, Digital Writers!"
    pattern = r"\*\*[A-Za-z]{3} \d{1,2}, \d{4}\*\*.*?Ahoy, Digital Writers!"
    # Replace found patterns with empty string, removing the matched content
    cleaned_content = re.sub(pattern, "", md_content, flags=re.DOTALL)
    return cleaned_content


def remove_after_names(md_content):
    logging.info("Removing content after names")
    # Regular expression to match the names and everything that follows
    # The pattern uses the names as the starting point and matches everything after them
    pattern = r"_Nicolas Cole_.*?\n(\* \* \*).*"

    # Replace the matched content with empty string, effectively removing it
    cleaned_content = re.sub(pattern, "", md_content, flags=re.DOTALL)
    return cleaned_content


def remove_phrases(md_content):
    logging.info("Removing phrases")
    # Define a pattern that matches "ship 30 for 30" or "typeshare" case-insensitively
    pattern = r"ship 30 for 30|typeshare"
    # Use re.sub() to replace the matched phrases with an empty string
    # The flag re.IGNORECASE makes the search case-insensitive
    cleaned_content = re.sub(pattern, "", md_content, flags=re.IGNORECASE)
    return cleaned_content


def remove_all(md_content):
    logging.info("Removing all")
    cleaned_content = remove_image_links(md_content)
    cleaned_content = remove_any_date_to_title(cleaned_content)
    cleaned_content = remove_after_names(cleaned_content)
    cleaned_content = remove_phrases(cleaned_content)
    return cleaned_content


def clean_md_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            cleaned_content = remove_all(content)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_content)


if __name__ == "__main__":
    # Get the path to the root of the project folder
    root_project_folder = pathlib.Path(__file__).parent.parent.resolve()
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Clean Markdown files")

    # Add an argument to the parser
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        help="The directory containing the Markdown files",
    )

    # Parse the arguments
    args = parser.parse_args()

    clean_md_files(f"{root_project_folder}/{args.directory}")
