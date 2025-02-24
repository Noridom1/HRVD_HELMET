import os

# Specify the folder containing the txt files
folder_path = "yolov9/data_ext/labels/val"  # Change this to your actual folder path

# Process all txt files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r") as file:
            lines = file.readlines()

        # Modify each line: replace the first value (label) with "1"
        modified_lines = ["0 " + " ".join(line.split()[1:]) + "\n" for line in lines]

        # Write the modified content back to the file
        with open(file_path, "w") as file:
            file.writelines(modified_lines)

print("All labels changed to 0 successfully!")
