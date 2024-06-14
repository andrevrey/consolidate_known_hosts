## Consolidate SSH Known Hosts

This Python script consolidates entries in the `.ssh/known_hosts` file, combining FQDN, hostname, and IP address entries for the same server into a single line. It ensures a cleaner and more manageable `known_hosts` file by reducing redundancy.

### Features
- **Consolidation**: Merges duplicate host entries into a single line.
- **Backup**: Automatically creates a timestamped backup of the original `known_hosts` file before making any changes.
- **Feedback**: Provides detailed feedback on the changes made during consolidation.

### Usage
1. Clone the repository or download the script.
2. Run the script from the command line, specifying the path to your `known_hosts` file:
   ```sh
   python consolidate_known_hosts.py /path/to/your/known_hosts
