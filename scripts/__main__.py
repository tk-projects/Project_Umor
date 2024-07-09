
import argparse
from view_database import print_database
from read_sensor import read_sensor

def main():
    parser = argparse.ArgumentParser(description="Execute specific functions.")
    parser.add_argument('--print_database', action='store_true', help="Print the database content")
    parser.add_argument('--read_sensor', action='store_true', help="Read sensor data")
    
    args = parser.parse_args()

    if args.print_database:
        print_database()
    
    if args.read_sensor:
        read_sensor()


if __name__ == "__main__":
    main()