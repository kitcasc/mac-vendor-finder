# MAC Address Vendor Lookup Tool

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)

A Python GUI application that identifies hardware manufacturers from MAC addresses, with automatic local MAC address detection capability.

## Features

- 🖥️ Automatic detection of local MAC addresses
- 🔍 Query vendor information from IEEE OUI database
- ⬇️ Download/update the latest OUI database
- 🖱️ Simple and intuitive GUI interface
- 🚀 Cross-platform support (Windows, Linux, macOS)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mac-vendor-lookup.git
   cd mac-vendor-lookup

2. Install required dependencies:
   ```bash
   pip install requests

3. Run the script:
   ```bash
   python mac_lookup.py

### Usage
# Manual Query:

Enter any MAC address in the input field (format like 00:1A:2B:3C:4D:5E)

Click "Query Manufacturer" button

# Auto-fill Local MAC:

Click "Auto-fill Local MAC" to automatically detect and fill your system's MAC address

# Update Database:

Click "Download/Update OUI database" to get the latest vendor information

### How It Works
# The application:

Uses multiple methods to detect local MAC addresses (UUID and system commands)

Downloads the official OUI database from IEEE (if not present)

Parses the MAC address to extract the OUI (Organizationally Unique Identifier)

Looks up the OUI in the database to find the vendor information

## Supported MAC Address Formats
The tool accepts MAC addresses in various formats:

00:1A:2B:3C:4D:5E

00-1A-2B-3C-4D-5E

001A2B3C4D5E

## Limitations
Requires internet connection for initial database download

Virtual MAC addresses may not be detected correctly

Some network interfaces might not be detected
