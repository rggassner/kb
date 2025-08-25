
#!/usr/bin/python3
import requests
import re
import zipfile
import csv
import os

def download_file(url, local_path):
    """Download a file from a given URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a ZIP file to a specified directory."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"ZIP file extracted to {extract_to}")
    except zipfile.BadZipFile as e:
        print(f"Error uncompressing the file: {e}")

def parse_hostfile(url, output_path):
    """Download and parse the threat host file, saving extracted domains to a YAML file."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        pattern = re.compile(r"127\\.0\\.0\\.1\\s+(.*)")
        
        with open(output_path, 'w') as file:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    match = pattern.match(line)
                    if match:
                        domain_name = match.group(1)
                        file.write(f'"{domain_name}": "YES"\n')
        print(f"Threat host file saved to {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the host file: {e}")

def preprocess_line(line):
    """Preprocess a CSV line by removing extra spaces after commas."""
    return line.replace(", ", ",")

def parse_csv(file_path, output_dir):
    """Parse a CSV file and save different fields into YAML files."""
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = {
        "malware.yml": 2,
        "threat_type.yml": 4,
        "malware_key.yml": 5,
        "malware_alias.yml": 6,
        "malware_printable.yml": 7,
        "confidence_level.yml": 9,
        "reference.yml": 10
    }
    
    file_handlers = {name: open(os.path.join(output_dir, name), 'w') for name in output_files}
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            preprocessed_lines = [preprocess_line(line) for line in csv_file]
            csv_reader = csv.reader(preprocessed_lines, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            for line_number, row in enumerate(csv_reader, start=1):
                if line_number >= 10 and len(row) > 9:
                    for file_name, column_index in output_files.items():
                        value = row[column_index] if column_index < len(row) else ""
                        file_handlers[file_name].write(f'"{row[2]}": "{value}"\n')
        
        print(f"CSV data processed and saved to {output_dir}")
    finally:
        for handler in file_handlers.values():
            handler.close()

if __name__ == "__main__":
    threat_host_url = "https://threatfox.abuse.ch/downloads/hostfile/"
    zip_url = "https://threatfox.abuse.ch/export/csv/domains/full/"
    local_zip_path = "threatfox.zip"
    extract_path = "output"
    csv_file_path = os.path.join(extract_path, "full_domains.csv")
    output_dir = "."
    
    parse_hostfile(threat_host_url, os.path.join(output_dir, "threats.yml"))
    
    if download_file(zip_url, local_zip_path):
        extract_zip(local_zip_path, extract_path)
        parse_csv(csv_file_path, output_dir)
