import os
import csv

class DatasetLoader:
    def __init__(self, data_path):
        """
        Sets the path where the data files are stored.
        """
        self.data_path = data_path

    def load_csv(self, file_name):
        """
        Loads a CSV file and returns the data as a list of rows.

        Args:
            file_name (str): The name of the CSV file to load.

        Returns:
            list: List of rows from the CSV file.
        """
        data = []
        try:
            file_path = os.path.join(self.data_path, file_name)
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
            print(f"✅ Successfully loaded {file_name} as CSV.")
        except FileNotFoundError:
            print(f"❌ Error: The file {file_name} was not found.")
        except Exception as e:
            print(f"❌ Error loading {file_name}: {e}")
        return data

    def load_attribute_names(self, file_name):
        """
        Loads attribute names from a .names file.

        Args:
            file_name (str): The name of the file to read attributes from.

        Returns:
            list: List of attribute names.
        """
        attributes = []
        try:
            file_path = os.path.join(self.data_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()

                start_reading = False
                for line in lines:
                    line = line.strip()

                    # Start when "1. a1" line is found
                    if line.startswith("1. a1:"):
                        start_reading = True

                    if start_reading:
                        if line and '.' in line and ':' in line:
                            parts = line.split('. ')
                            if len(parts) > 1:
                                attribute_name = parts[1].split(':')[0]
                                attributes.append(attribute_name)
                        # Stop if we reach "43. Class:"
                        if line.startswith("43. Class:"):
                            break

            print(f"✅ Successfully loaded attributes from {file_name}.")
        except FileNotFoundError:
            print(f"❌ Error: The file {file_name} was not found.")
        except Exception as e:
            print(f"❌ Error loading {file_name}: {e}")
        return attributes

    def load_names(self, file_name):
        """
        Just calls load_attribute_names to keep things consistent.
        """
        return self.load_attribute_names(file_name)

# Usage
if __name__ == "__main__":
    data_loader = DatasetLoader(data_path="connect4_dataset")

    csv_data = data_loader.load_csv('connect-4.data.csv')
    print("First 5 rows of CSV:", csv_data[:5])

    attribute_names = data_loader.load_attribute_names('connect-4.names.txt')
    print("Attributes (from load_attribute_names):", attribute_names)

    # Using the new load_names method
    attributes_via_load_names = data_loader.load_names('connect-4.names.txt')
    print("Attributes (from load_names):", attributes_via_load_names)
