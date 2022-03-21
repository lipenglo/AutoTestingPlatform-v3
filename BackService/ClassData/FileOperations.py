from shutil import copy

# Create reference here.
from ClassData.Logger import Logging
from ClassData.Common import Common

import os
import shutil

# Create info here.
cls_Logging = Logging()
cls_Common = Common()


# 文件操作
class FileOperations(object):
    # 把文件保存在临时目录
    def file_to_path(self, fileObj):
        results = {}
        tempPath = f"{os.path.abspath('.')}/_DataFiles/Temp/"
        try:
            splitStr = fileObj['file'].name.split('.')
            if len(splitStr) >= 2:
                fileSuffix = splitStr[-1]
            else:
                fileSuffix = ""
            if fileSuffix:
                fileName = f'{cls_Common.generate_only_code()}.{fileSuffix}'
            else:
                fileName = cls_Common.generate_only_code()
            fliePath = f'{tempPath}{fileName}'
            with open(fliePath, 'wb') as f:
                for line in fileObj['file'].chunks():
                    f.write(line)
        except BaseException as e:
            errorMsg = str(e)
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'file_to_path', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'file_to_path', errorMsg)
        else:
            results['state'] = True
            results['filePath'] = fliePath
            results['fileName'] = fileName
        return results

    def read_file(self, filePath):
        results = {}
        try:
            with open(filePath, 'r') as f:
                data = f.read()
        except BaseException as e:
            errorMsg = f'文件读取失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'read_file', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'read_file', errorMsg)
        else:
            results['state'] = True
            results['data'] = data
        return results

    # 判断该路径下是否有此文件夹 如果没有就新增
    def new_folder(self, path):
        results = {}
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except BaseException as e:
            errorMsg = f'创建文件夹失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'new_folder', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'new_folder', errorMsg)
        else:
            results['state'] = True
            results['path'] = path
        return results

    # 删除文件
    def delete_file(self, filePath):
        results = {}
        try:
            if os.path.exists(filePath):
                os.remove(filePath)  # 删除
            else:
                errorMsg = '目录文件不存在'
                results['state'] = False
                results['errorMsg'] = errorMsg
                cls_Logging.print_log('error', 'delete_file', errorMsg)
                cls_Logging.record_error_info('API', 'ClassData', 'delete_file', errorMsg)
        except BaseException as e:
            errorMsg = f'删除文件失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'delete_file', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'delete_file', errorMsg)
        else:
            results['state'] = True
        return results

    # 删除目录及以下目录文件
    def delete_folder(self, folderPath):
        results = {}
        try:
            if os.path.exists(folderPath):
                for fileList in os.walk(folderPath):
                    for name in fileList[2]:
                        os.remove(os.path.join(fileList[0], name))
                shutil.rmtree(folderPath)
            else:
                errorMsg = '目录不存在'
                results['state'] = False
                results['errorMsg'] = errorMsg
                cls_Logging.print_log('error', 'delete_folder', errorMsg)
                cls_Logging.record_error_info('API', 'ClassData', 'delete_folder', errorMsg)
        except BaseException as e:
            errorMsg = f'删除文件失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'delete_folder', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'delete_folder', errorMsg)
        else:
            results['state'] = True
        return results

    # 复制文件到指定目录
    def copy_file_to_dir(self, file, directory):
        results = {}
        try:
            shutil.copy(file, directory)
            newFilePath = f"{directory}/{file.split('/')[-1]}"
        except BaseException as e:
            errorMsg = f'文件复制失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'copy_file_to_dir', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'copy_file_to_dir', errorMsg)
        else:
            results['state'] = True
            results['newFilePath'] = newFilePath
        return results

    # 复制文件夹
    def copy_dir(self, dir, newdir):
        results = {}
        try:
            for p in os.listdir(dir):
                print(p)
                filepath = newdir + '/' + p
                oldpath = dir + '/' + p
                if os.path.isfile(oldpath):
                    copy(oldpath, filepath)
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"复制文件夹失败:{e}"
        else:
            results['state'] = True
        return results

    # 判断该路径下是否有此文件夹
    def is_folder(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    # 判断文件是否存在
    def is_flie(self,path):
        if os.path.exists(path):
            return True
        else:
            return False


    # 修改文件夹名称
    def rename_dir(self, src, dst):
        """
        :param src:要修改的目录名
        :param dst:修改后的目录名
        :return:
        """
        results = {}
        try:
            os.rename(src, dst)
        except BaseException as e:
            errorMsg = f'改名失败:{e}'
            results['state'] = False
            results['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'rename_dir', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData', 'rename_dir', errorMsg)
        else:
            results['state'] = True
            results['newPath'] = dst
        return results
