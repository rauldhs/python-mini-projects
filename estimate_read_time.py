"""
Scans files and directories to compute reading statistics based on reading speed.
"""

import os
import sys
import getopt
from os import listdir
from os.path import isfile, join
from datetime import timedelta
import fitz  # PyMuPDF
from colorama import init, Fore, Style

init(autoreset=True)

class Document:
    """
    Represents a document for reading statistics.

    Attributes:
        file_name (str): Document file path.
        reading_speed (int): Reading speed (words per minute).
        total_mins_to_read (float): Estimated reading time in minutes.
        total_formatted_time_to_read (str): Formatted reading time.
        total_words (int): Word count in the document.
        total_pages (int): Number of pages.
        name (str): Base name of the document file.
    """

    def __init__(self, file_name, reading_speed):
        """
        Initializes the document and calculates statistics.

        Args:
            file_name (str): Path to the document.
            reading_speed (int): Reading speed.
        """
        self.file_name = file_name
        self.reading_speed = reading_speed
        self.read_doc()

    def read_doc(self):
        """Calculates document statistics."""
        with fitz.open(self.file_name) as doc:
            text = "\n".join([page.get_text() for page in doc])
            self.total_words = len(text.split())
            self.total_mins_to_read = self.total_words / self.reading_speed
            self.total_formatted_time_to_read = format_time(self.total_mins_to_read)
            self.total_pages = doc.page_count
            self.name = os.path.basename(doc.name)


def format_time(minutes):
    """
    Formats time in hours, minutes, and seconds.

    Args:
        minutes (float): Time in minutes.

    Returns:
        str: Formatted time string.
    """
    td = timedelta(minutes=minutes)
    s = int(td.total_seconds())
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h} Hours {m} Minutes and {s} Seconds"


def scan_directory(directory, reading_speed, extensions,recursive):
    """
    Scans a directory and creates Document objects.

    Args:
        directory (str): Directory path.
        reading_speed (int): Reading speed.
        extensions (tuple): File extensions to include.

    Returns:
        list: List of Document objects.
    """
    documents = []
    
    if not recursive:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(extensions)]
        documents.extend([Document(os.path.join(directory, file), reading_speed) for file in files])
    else:
        for root, dirs, files in os.walk(directory):
            files = [f for f in files if f.endswith(extensions)]
            documents.extend([Document(os.path.join(root, file), reading_speed) for file in files])
    
    return documents

def print_documents_stats(all_documents):
    """
    Print statistics for a list of documents in a formatted table with colors.

    Args:
        all_documents (list): A list of document objects. Each document should have 
                              attributes `name`, `total_words`, `total_pages`, and `total_formatted_time_to_read`.
    """
    size = os.get_terminal_size().columns
    col1_width = size // 2
    col2_width = size // 10
    col3_width = size // 15
    col4_width = size // 4

    total_words = 0
    total_pages = 0
    total_minutes_time = 0
    # Header
    header = f"{Fore.MAGENTA}{'File Name':<{col1_width}} {Fore.BLUE}{'Words':<{col2_width}} {Fore.YELLOW}{'Pages':<{col3_width}} {Fore.GREEN}{'Estimated Reading Time':<{col4_width}}{Style.RESET_ALL}"
    print(header)
    print("=" * size)

    # Data rows
    for document in all_documents:
        # Truncate file name if too long
        if len(document.name) > col1_width:
            document.name = document.name[:col1_width - 3].rstrip() + "." * (col1_width - len(document.name))

        row = f"{Fore.MAGENTA}{document.name:<{col1_width}} {Fore.BLUE}{document.total_words:<{col2_width}} {Fore.YELLOW}{document.total_pages:<{col3_width}} {Fore.GREEN}{document.total_formatted_time_to_read:<{col4_width}}{Style.RESET_ALL}"
        print(row)
        
        total_words += document.total_words
        total_pages += document.total_pages
        total_minutes_time += document.total_mins_to_read
    
    total_reading_time = format_time(total_minutes_time)
    total_row = f"{Fore.MAGENTA}{'Total':<{col1_width}} {Fore.BLUE}{total_words:<{col2_width}} {Fore.YELLOW}{total_pages:<{col3_width}} {Fore.GREEN}{total_reading_time:<{col4_width}}{Style.RESET_ALL}"
    print("=" * size)
    print(total_row)
def main(argv):
    """
    Parses command-line arguments and prints reading statistics.

    Args:
        argv (list): Command-line arguments.
    """
    extensions = (".pdf", ".xps", ".epub", ".mobi", ".fb2", ".cbz", ".svg", ".txt")
    reading_speed = 200
    
    directories = ""
    files = ""
    recursive = False
    
    all_documents = []

    try:
        opts, args = getopt.getopt(argv, "hs:d:f:r", ["reading_speed=", "directories=", "files=","recursive"])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: script.py -s <reading_speed> -d <directories> -f <files>")
            sys.exit()
        elif opt in ("-s", "--reading_speed"):
            reading_speed = int(arg)
        elif opt in ("-r","--recursive"):
            recursive = True
        elif opt in ("-d", "--directories"):
            directories = arg
        elif opt in ("-f", "--files"):
            files = arg
            
    for directory in directories.split(","):
            all_documents.extend(scan_directory(directory, reading_speed, extensions,recursive))
    for file in files.split(","):
                if file.endswith(extensions):
                    all_documents.append(Document(file, reading_speed))
                else:
                    print("Unsupported file format.")
    print_documents_stats(all_documents)
   
if __name__ == "__main__":
    main(sys.argv[1:])
