from ftplib import FTP

import pandas as pd

import tempfile
import platform
import chardet
import zipfile
import re
import os

def map_files(ftp_client: FTP, base_path: str) -> dict:
    ftp_client.cwd(base_path)
    files_by_years = {int(i): {} for i in ftp_client.nlst() if re.fullmatch(r"\d{4}", i)}

    for year in files_by_years.keys():
        ftp_client.cwd(f"{base_path}/{year}")
        file_list = ftp_client.nlst()

        files_by_years[year] = {int(i.split("_")[1][1:2]): i for i in file_list}

    return files_by_years

def download_data(year: int, trimestre: int) -> dict:
    if not (isinstance(year, (int, float, str)) and isinstance(trimestre, (int, float, str))):
        raise TypeError("The value of year and trimestre must be 'int', 'float' or 'str'.")

    try:
        year = int(year)
        trimestre = int(trimestre)
    except ValueError:
        return print("The value of year and trimestre must can be convertible into integer!")

    if not trimestre in [1, 2, 3, 4]:
        raise ValueError("The trimestre value must be 1, 2, 3 or 4")

    base_path = "/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados"

    ftp_client = FTP("ftp.ibge.gov.br", timeout = 600)
    ftp_client.login()
    
    files_dict = map_files(ftp_client= ftp_client, base_path = base_path)

    file_name = files_dict.get(year, {}).get(trimestre)
    if file_name is None:
        return print(f"This data file for {year} year {trimestre} trimestre doesnt exist")
    print("Start download data...")

    filepath_download = f"{base_path}/{year}/{file_name}"
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        local_file_path_data = temp_file.name
        ftp_client.retrbinary(f"RETR {filepath_download}", temp_file.write)
    
    ftp_client.cwd(f"{base_path}/Documentacao")
    dicionario_file = [i for i in ftp_client.nlst() if "dicionario" in i.lower()]
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        local_file_path_dict = temp_file.name
        ftp_client.retrbinary(f"RETR {base_path}/Documentacao/{dicionario_file[0]}", temp_file.write)

    print(f"Done!")
    return {
        "dicionario_path": local_file_path_dict,
        "data_path": local_file_path_data,
    }

def extract_data(paths: dict) -> pd.DataFrame:
    if not isinstance(paths, dict):
        raise TypeError("The paths arguument of extract_data must be a dict.")
    
    if platform.system() == "Windows":
        temp_dir = os.path.join(os.getenv("TEMP"), "dicionarios_extraidos")
    else:
        temp_dir = "/tmp/dicionarios_extraidos"

    print("Starting data extraction... ")
    with zipfile.ZipFile(paths.get("dicionario_path"), "r") as zip_ref:
        files_in_folder = zip_ref.namelist()
        sas_files = [i for i in files_in_folder if i.endswith(".sas")]
        if len (sas_files) > 1: 
            return print("Deu merda!")
        
        file_name_sas = sas_files[0]
        zip_ref.extract(file_name_sas, path = temp_dir)

    with zipfile.ZipFile(paths.get("data_path"), "r") as zip_ref:
        files_in_folder = zip_ref.namelist()
        txt_files = [i for i in files_in_folder if i.endswith(".txt")]
        if len(txt_files) > 1:
            return print("Deu merda!")
        
        file_name_txt = txt_files[0]
        zip_ref.extract(file_name_txt, path = temp_dir)

    for p in paths.values():
        os.remove(p)
    
    print("Done!")
    return {
        "dicionario_sas": os.path.join(temp_dir, file_name_sas),
        "data_txt": os.path.join(temp_dir, file_name_txt)
    }

def parse_sas_file(sas_file: str, selected_columns: list[str]|None = None) -> tuple[list, str]:
    columns = []
    
    # Descobrindo sas encoding
    with open(sas_file, "rb") as f:
        result = chardet.detect(f.read())
        encoding = result["encoding"] or "utf8"
        
    with open(sas_file, 'r', encoding=encoding) as f:
        for line in f:
            splited_line = line.split()
            if not line[0].startswith("@"): continue
            
            nome_col = splited_line[1]
            start_pos = int(splited_line[0].replace("@", "")) - 1
            end_pos = start_pos + int(splited_line[2].replace("$", "").replace(".", ""))

            if selected_columns is None or nome_col in selected_columns:
                columns.append((nome_col, start_pos, end_pos))

    if isinstance(selected_columns, (list)) and len(columns) != len(selected_columns):
        print(selected_columns)
    return columns, encoding

def create_dataframe(dict_paths: dict, columns_intrested: list[str], sample_size: float|None = None, random_seed: int|None = None) -> pd.DataFrame|None:
    if (not sample_size is None) and (not isinstance(sample_size, float) or sample_size > 1 or sample_size < 0):
        raise TypeError("sample_size must be a float between 0 and 1. or None")
    
    if not columns_intrested is None and not isinstance(columns_intrested, list):
        raise TypeError("The columns_intrested argument must be a list or None")
    else:
        if sum([0 if isinstance(i, str) else 1 for i in columns_intrested]) > 0:
            raise TypeError("The values in columns intrested must be of tpe str")

    columns, *_ = parse_sas_file(sas_file=dict_paths.get("dicionario_sas"), selected_columns=columns_intrested)
    col_names = [col[0] for col in columns]
    col_specs = [(col[1], col[2]) for col in columns]

    df_iter = pd.read_fwf(dict_paths.get("data_txt"), colspecs=col_specs, names=col_names, chunksize=100_000)
    
    dataframes_list = list()
    for chunk in df_iter:
        sample: pd.DataFrame = chunk.sample(frac= sample_size, random_state = random_seed)
        dataframes_list.append(sample)
    
    return pd.concat(dataframes_list, ignore_index=True)
    

if __name__ == "__main__":
    dict_infos = download_data(year=2019, trimestre=3)
    extract_data(dict_infos, columns_intrested=[""])