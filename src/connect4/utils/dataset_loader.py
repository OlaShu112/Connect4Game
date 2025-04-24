import os
import csv
import json
import numpy as np

class DatasetLoader:
    def __init__(self, data_path):
        """
        Initializes the DatasetLoader with the provided data path.
        :param data_path: The path to the dataset folder or file.
        """
        self.data_path = data_path

    def load_csv(self, file_name):
        """
        Loads a CSV file and returns it as a list of dictionaries.
        :param file_name: The name of the CSV file to load.
        :return: List of dictionaries containing the data.
        """
        data = []
        try:
            file_path = os.path.join(self.data_path, file_name)
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            print(f"Successfully loaded {file_name} as CSV.")
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found.")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
        return data

    def load_json(self, file_name):
        """
        Loads a JSON file and returns the parsed data.
        :param file_name: The name of the JSON file to load.
        :return: Parsed JSON data.
        """
        try:
            file_path = os.path.join(self.data_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
            print(f"Successfully loaded {file_name} as JSON.")
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {file_name} could not be decoded as JSON.")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
        return data

    def load_numpy(self, file_name):
        """
        Loads a NumPy dataset (usually a `.npy` file).
        :param file_name: The name of the numpy file to load.
        :return: NumPy array.
        """
        try:
            file_path = os.path.join(self.data_path, file_name)
            data = np.load(file_path)
            print(f"Successfully loaded {file_name} as a NumPy array.")
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found.")
        except ValueError:
            print(f"Error: The file {file_name} could not be loaded as a NumPy array.")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
        return data

# Example usage:
if __name__ == "__main__":
    # Set your data directory path
    data_loader = DatasetLoader(data_path="path_to_your_dataset")

    # Example of loading CSV
    csv_data = data_loader.load_csv('game_data.csv')
    print(csv_data)

    # Example of loading JSON
    json_data = data_loader.load_json('config.json')
    print(json_data)

    # Example of loading NumPy data
    numpy_data = data_loader.load_numpy('game_state.npy')
    print(numpy_data)
