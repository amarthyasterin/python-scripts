import boto3
from collections import defaultdict

# Initialize the S3 client
s3 = boto3.client('s3')

# Specify the bucket and prefix (location)
bucket_name = 'doc'
prefix = 'live/docok/check/'

# List objects in the specified bucket and prefix
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Check if there are any files in the location
if 'Contents' not in response:
    print("No files found in the specified location.")
    exit()

# Extract file sizes and keys
files = [{'Key': obj['Key'], 'Size': obj['Size']} for obj in response['Contents']]

# Sort files by size
files.sort(key=lambda x: x['Size'], reverse=True)

# Function to calculate average size
def calculate_average_size(file_list):
    total_size = sum(file['Size'] for file in file_list)
    return total_size / len(file_list)

# Categorize files
def categorize_files(file_list):
    avg_size = calculate_average_size(file_list)
    highest = file_list[:3]
    lowest = file_list[-3:]
    avg_files = [file for file in file_list if abs(file['Size'] - avg_size) == min(abs(f['Size'] - avg_size) for f in file_list)]
    
    # Ensure we only get 3 average files
    avg_files = avg_files[:3]
    
    return highest, avg_files, lowest

# Get categorized files
highest_files, avg_files, lowest_files = categorize_files(files)

# Print results
print("Top 3 Largest Files:")
for file in highest_files:
    print(f"File: {file['Key']}, Size: {file['Size']} bytes")

print("\nTop 3 Average Files:")
for file in avg_files:
    print(f"File: {file['Key']}, Size: {file['Size']} bytes")

print("\nTop 3 Smallest Files:")
for file in lowest_files:
    print(f"File: {file['Key']}, Size: {file['Size']} bytes")
