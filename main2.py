import streamlit as st
import os
import json
import pandas as pd
import shutil

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def convert_to_json_from_excel(file, rows):
    working_path = os.getcwd()
    excel_folder = os.path.join(working_path, 'excel_folder')
    output_folder = os.path.join(working_path, 'output')
    create_directory(excel_folder)
    create_directory(output_folder)

    # Save the uploaded file to the excel folder
    file_path = os.path.join(excel_folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())

    # Perform the conversion to JSON
    df = pd.read_excel(file_path, nrows=rows, dtype=str)
    converted_filename = os.path.splitext(file.name)[0]
    converted_file_path = os.path.join(output_folder, f"{converted_filename}.json")
    df.to_json(converted_file_path, orient='records', indent=2)

    return converted_filename

def convert_to_json_from_csv(file, rows):
    working_path = os.getcwd()
    csv_folder = os.path.join(working_path, 'csv_folder')
    output_folder = os.path.join(working_path, 'output')
    create_directory(csv_folder)
    create_directory(output_folder)

    # Save the uploaded file to the csv folder
    file_path = os.path.join(csv_folder, file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())

    # Perform the conversion to JSON
    df = pd.read_csv(file_path, nrows=rows, dtype=str)
    converted_filename = os.path.splitext(file.name)[0]
    converted_file_path = os.path.join(output_folder, f"{converted_filename}.json")
    df.to_json(converted_file_path, orient='records', indent=2)

    return converted_filename

def clear_directory(directory):
    folder_path = os.path.join(os.getcwd(), directory)
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def main():
    st.title("Daddy Chill XLSX to JSON")
    gif_url = "https://media.giphy.com/media/yiADANv89n7UQuS5kJ/giphy.gif"
    st.image(gif_url, use_column_width=True)

    # # Embedding GIF from local file path
    # gif_path = "path/to/example.gif"
    # st.image(gif_path, use_column_width=True)


    uploaded_file = st.file_uploader("Upload a file", type=['xlsx', 'csv'], accept_multiple_files=False, key="fileUploader")
    if uploaded_file is not None:
        rows = st.number_input("Number of rows", value=10)
        if st.button("Convert"):
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()

            if file_extension == '.xlsx':
                converted_filename = convert_to_json_from_excel(uploaded_file, rows)
            elif file_extension == '.csv':
                converted_filename = convert_to_json_from_csv(uploaded_file, rows)
            else:
                st.error("Unsupported file format")
                return

            converted_file_path = os.path.join('output', f"{converted_filename}.json")
            st.success(f"File converted successfully.")

            # Provide a download button for the converted file
            download_button_str = f"Download Converted File ({converted_filename}.json)"
            with open(converted_file_path, "r") as f:
                file_contents = f.read()
            st.download_button(
                label=download_button_str,
                data=file_contents,
                file_name=f"{converted_filename}.json",
                mime="application/json"
            )

    if st.button("Clear Files"):
        directories = ['output', 'excel_folder', 'csv_folder']
        for directory in directories:
            clear_directory(directory)
        st.success("Files cleared successfully.")

if __name__ == '__main__':
    main()
