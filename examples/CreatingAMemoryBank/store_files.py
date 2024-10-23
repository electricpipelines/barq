import argparse
from dabarqus import barq
import sys
import os

def main():
    print(sys.argv)
    parser = argparse.ArgumentParser(description="Store documents using Dabarqus SDK")
    parser.add_argument("--memory-bank", required=True, help="Name of the memory bank")
    parser.add_argument("--input-path", required=True, help="Path to the input file or directory")
    parser.add_argument("--no-override", action="store_true", help="Add random number to the file name to avoid override")
    parser.add_argument("--server-url", default="http://localhost:6568", help="Dabarqus server URL")
    args = parser.parse_args()

    # Initialize the SDK
    sdk = barq(args.server_url)

    # Check the health of the service
    health = sdk.check_health()
    print(f"Service health: {health}")

    memory_bank_name = args.memory_bank

    if args.no_override:
        # Add random number to the file name to avoid override
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        memory_bank_name = args.memory_bank + random_string

    # Convert input path to absolute path if it's relative
    input_path = args.input_path
    if not os.path.isabs(input_path):
        input_path = os.path.abspath(input_path)
    
    print(f"Using absolute input path: {input_path}")

    # Enqueue ingestion
    ingestion_result = sdk.enqueue_ingestion(memory_bank_name=memory_bank_name, input_path=input_path, overwrite=True)
    print(f"Ingestion result: {ingestion_result}")

    # Wait until the ingestion is completed
    ingestions = sdk.check_ingestion_progress(memory_bank_name)
    while ingestions["status"] != "complete":
        ingestions = sdk.check_ingestion_progress(memory_bank_name)
        sys.stdout.write(f"Ingestion progress: {ingestions['progress']:.2f}% \r")
        sys.stdout.flush()
    print(f"Ingestion complete!")

if __name__ == "__main__":
    main()