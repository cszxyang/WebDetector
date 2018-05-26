import os
static_dir = "/static/results"
root_dir_path = os.path.abspath('.') + static_dir


def get_one_day_img(date):
    l = []
    sub_dirs_path = os.listdir(root_dir_path)
    for dir_path in sub_dirs_path:
        if dir_path == date:
            d = {}
            result_list = get_img_list(dir_path)
            d["date"] = date
            d["data"] = result_list
            l.append(d)
    return l


def get_all():
    l = []
    sub_dirs_path = os.listdir(root_dir_path)
    for dir_path in sub_dirs_path:
        d = {}
        result_list = get_img_list(dir_path)
        d["date"] = dir_path
        d["data"] = result_list
        l.append(d)
    return l


def get_img_list(dir_path):
    full_sub_path = os.path.join(root_dir_path, dir_path)
    img_list = os.listdir(full_sub_path)
    result = []
    for img_path in img_list:
        result.append("/results/"+ dir_path + "/" + img_path)
    return result

