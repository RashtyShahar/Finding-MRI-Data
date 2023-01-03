import os
import pydicom
import shutil
from shutil import ignore_patterns, copy
from re import search

path = r'C:\Users\shahar.rashty\Desktop\testing'
SearchedBodyPart = 'knee'

def findScans(path:str,SearchedBodyPart:str):
    '''
    finds paths to mri scans of the a body part based on DICOM tags
    :param path: path to directory to be searched
    :param SearchedBodyPart: what body part to look for for example 'knee'
    :return:
    '''
    folders_list = []
    for root, subdirs, files in os.walk(path):
        if not files:
            continue
        else:
            try:
                ds = pydicom.dcmread(os.path.join(root, files[0]), force=True)
                study_desc = ds.get("StudyDescription", "").lower()
                series_desc = ds.get('SeriesDescription', "").lower()
                body_part = ds.get("BodyPartExamined", "").lower()
                if SearchedBodyPart in study_desc or \
                        SearchedBodyPart in series_desc or \
                        SearchedBodyPart in body_part:
                    print(root)
                    folders_list.append(root)
            except:
                continue
    return folders_list

def copy_to_dst(folders_list,destination):
    '''
    copies all folders from folders_list to destination folder that will be created on desktop and
    keeps the name of origin folder with added numbering
    :param folders_list:list contains paths to MRI scans
    :destination:name for the new parent folder that will be created on desktop
    :return:
    '''
    for i in range(len(folders_list)):
        folder_name = folders_list[i].split("\\")[-1]
        dst = f"C:\\Users\\shahar.rashty\\Desktop\\{destination}_{SearchedBodyPart}\\{folder_name} -- {i}"
        shutil.copytree(folders_list[i],dst , ignore=ignore_patterns('*.MVbin' ,'localizer.','1.3.6.*'),copy_function = copy)

root = r"C:\Users\shahar.rashty\Desktop\MSK tmp\unclean_elbow"
stringstoremove = ["^1\.3\.6." , "iQMR", "localizer"]
# stringstoremove = ["^1\.3\.6." , "Sharp","Default", "Soft"]

def remove_processed(root:str,stringstoremove:list):
    '''
    remove processed series based on folder name - all folders that contains values that appears on stringstoremove list will be deleted.
    :param root: folder contains subfolders with MRI series
    :param stringstoremove: list of strings that will be searched at each root's subfolders name
    :return:
    '''
    for path, subdirs, files in os.walk(root):
        for subdir_name in subdirs:
            file_path = os.path.join(path, subdir_name)
            # print(file_path)
            for string in stringstoremove:
                if search(string, subdir_name):
                    shutil.rmtree(file_path)




body_lst=findScans(path,SearchedBodyPart)
copy_to_dst(body_lst,'MRI')
remove_processed(r'C:\Users\shahar.rashty\Desktop\MRI_knee',stringstoremove)

'''
final result - at desktop will be created 'MRI_bodypart' folder with all MRI scans of the bodyPart cleaned from processed series 
'''