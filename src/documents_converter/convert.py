from pathlib import Path

import requests


def convert(file_name, target_extension):
    r"""Переводит указанный файл в файл с нужным расширением

    http://dag.wiee.rs/home-made/unoconv/

    :param file_name: путь к файлу, который надо перевести в другой формат
    :param target_extension: целевой формат файла
    """
    ext = Path(file_name).suffix.strip('.')
    files = {'file': (file_name, open(file_name, 'rb'), ext)}

    url = f'https://unoconv.cloud.cpur.ru/unoconv/{target_extension}'
    try:
        response = requests.post(url, files=files)
    except requests.RequestException as e:
        print(e)
        return None
    else:
        return response.content
