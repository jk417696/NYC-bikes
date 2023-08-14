import os

# best option: script using argparse with year and func as params


def iterate_over_files_year(year: str, df_func):
    """
    :param year: year to analyse
    :param df_func: function that produces output with a structure same as in "parse_local_csv_file"
    """
    directory_path = 'data/' + year
    files = os.listdir(directory_path)
    files = sorted(files)
    for file in files:
        if os.path.isfile(os.path.join(directory_path, file)):
            month = str(file[:6])
            # df_func(month)


def iterate_over_all_files(df_func):
    directory_path = 'data/'
    years = os.listdir(directory_path)
    years = sorted(years)
    for year in years:
        iterate_over_files_year(year, df_func)


# iterate_over_files_year('2015', )


