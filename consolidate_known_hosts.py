import re
import argparse
import shutil
from collections import defaultdict
from datetime import datetime

def read_known_hosts(file_path):
    """
    Reads the known_hosts file and returns its lines.

    Args:
        file_path (str): The path to the known_hosts file.

    Returns:
        list: A list of lines from the known_hosts file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def parse_known_hosts(lines):
    """
    Parses the lines from the known_hosts file and groups host entries by their key parts.

    Args:
        lines (list): A list of lines from the known_hosts file.

    Returns:
        defaultdict: A dictionary with key parts as keys and a list of host parts as values.
    """
    hosts = defaultdict(list)
    for line in lines:
        if line.strip() and not line.startswith('#'):  # Skip empty lines and comments
            host_part = line.split()[0]
            key_part = ' '.join(line.split()[1:])
            hosts[key_part].append(host_part)
    return hosts

def consolidate_hosts(hosts):
    """
    Consolidates the host entries into single lines for each unique key part.

    Args:
        hosts (defaultdict): A dictionary with key parts as keys and a list of host parts as values.

    Returns:
        list: A list of consolidated lines.
    """
    consolidated_lines = []
    for key_part, host_parts in hosts.items():
        consolidated_line = ','.join(host_parts) + ' ' + key_part  # Combine host parts into a single line
        consolidated_lines.append(consolidated_line)
    return consolidated_lines

def write_known_hosts(file_path, lines):
    """
    Writes the consolidated lines back to the known_hosts file.

    Args:
        file_path (str): The path to the known_hosts file.
        lines (list): A list of lines to write to the file.
    """
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def create_backup(file_path):
    """
    Creates a backup of the known_hosts file with a timestamp.

    Args:
        file_path (str): The path to the known_hosts file.

    Returns:
        str: The path to the backup file.
    """
    backup_path = file_path + '.bak.' + datetime.now().strftime('%Y%m%d%H%M%S')
    shutil.copy2(file_path, backup_path)  # Copy the file to a backup location
    print(f"Backup created at: {backup_path}")
    return backup_path

def consolidate_known_hosts(file_path):
    """
    Consolidates entries in the known_hosts file, creating a backup before processing.

    Args:
        file_path (str): The path to the known_hosts file.
    """
    backup_path = create_backup(file_path)  # Create a backup of the file
    lines = read_known_hosts(file_path)  # Read the original file
    original_line_count = len(lines)  # Count the original lines
    hosts = parse_known_hosts(lines)  # Parse the lines into host entries
    consolidated_lines = consolidate_hosts(hosts)  # Consolidate the host entries
    consolidated_line_count = len(consolidated_lines)  # Count the consolidated lines
    write_known_hosts(file_path, consolidated_lines)  # Write the consolidated lines back to the file
    
    # Provide feedback on the changes made
    print(f"Original number of lines: {original_line_count}")
    print(f"Consolidated number of lines: {consolidated_line_count}")
    if original_line_count != consolidated_line_count:
        print("Consolidation complete. The following changes were made:")
        for old_line, new_line in zip(lines, consolidated_lines):
            if old_line.strip() != new_line.strip():  # Check for changes in the lines
                print(f"- {old_line.strip()} -> {new_line.strip()}")
    else:
        print("No changes were necessary; the file was already consolidated.")

if __name__ == "__main__":
    # Setup argument parser for command-line usage
    parser = argparse.ArgumentParser(description="Consolidate entries in the .ssh/known_hosts file.")
    parser.add_argument("file_path", help="Path to the known_hosts file")
    args = parser.parse_args()

    consolidate_known_hosts(args.file_path)  # Run the consolidation function with the provided file path
