import requests
from download import maybe_download_and_extract

# The direct link to the Kaggle data set
data_url = 'https://www.kaggle.com/alexattia/the-simpsons-characters-dataset/downloads/simpsons_dataset.tar.gz/4'

# The local path where the data set is saved.
local_dir_name = "./dataset"

maybe_download_and_extract(data_url, local_dir_name)