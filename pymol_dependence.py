#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        :auto.py
@Description:       :自动处理脚本
@Date     :2021/09/02 15:19:15
@Author      :hotwa
@version      :1.0
resource: https://www.cnblogs.com/wq242424/p/13073222.html
http://blog.sina.com.cn/s/blog_7188922f0100wbz1.html
https://www.jianshu.com/p/3396e94315cb
https://blog.csdn.net/dengximo9047/article/details/101221495 # 疏水表面
http://www.mdbbs.org/thread-4064-1-1.html # 用来寻找配体口袋的残基
'''
import os
from pymol import cmd
from pathlib import Path

l = ['5LWM','5E93','5EA9','5ZZ4','6GXY','6GXG']
path = 'H:\\CovInDB\\code\\CovInDB\\crawler\\2021\\pdbfile'

# select ligand, resn x
def autogo():
    for i in l:
        file = os.path.join(path,i)
        cmd.load(file)
        cmd.remove('solvent')
        cmd.reinitialize()

# error class
class PathError(BaseException):
    def __init__(self,arg):
        self.arg = arg

class moleculeidentity():
    """moleculeidentity [summary]

    [识别pdb蛋白文件中的小分子标识符]
    """
    def __init__(self,pdbfile,path):
        self.pathstr = path
        self.path = Path(path)
        self.pdbfile = pdbfile
        self.init()

    def init(self):
        if not self.path.exists():
            raise PathError('path not exist')
        listoffile =  list(self.path.glob('*.pdb'))
        self.path_parent = listoffile[0].parent
        self.pdbfilelist = [i.name for i in listoffile]

    def __parse_pdb_ligid(self,ion=True):
        if self.pdbfile not in self.pdbfilelist:
            raise FileNotFoundError(f'not found {self.pdbfile} in {self.path}')
        infos_line = []
        ligId = []
        for i in self.__generate_pdb_lines():
            if self.check_line_header(i) == 'HET':
                infos_line.append(i)
        ligId = [i.split()[1] for i in infos_line]
        ligId = list(set(ligId))
        if not ion: ligId = [i for i in ligId if len(i) == 3 ] # remove ion from list
        return ligId
    
    @property
    def ligId(self):
        return self.__parse_pdb_ligid()

    @staticmethod
    def check_line_header(line_text):
        return line_text[0:6].strip()
            
    def __generate_pdb_lines(self):
        for row in open(self.path_parent.joinpath(self.pdbfile),'r+'):
            yield row.strip()
