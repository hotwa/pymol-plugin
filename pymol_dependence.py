#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        :auto.py
@Description:       :自动处理脚本
@Date     :2021/09/02 15:19:15
@Author      :hotwa
@version      :1.0
https://zhuanlan.zhihu.com/p/121215784 # PyMOL 选择器的语法参考
https://blog.csdn.net/u011450367/article/details/51815130
resource: https://www.cnblogs.com/wq242424/p/13073222.html
http://blog.sina.com.cn/s/blog_7188922f0100wbz1.html
https://www.jianshu.com/p/3396e94315cb
https://blog.csdn.net/dengximo9047/article/details/101221495 # 疏水表面
http://www.mdbbs.org/thread-4064-1-1.html # 用来寻找配体口袋的残基
'''

from pymol import cmd
from pathlib import Path


l = ['5LWM','5E93','5EA9','5ZZ4','6GXY','6GXG']
path = 'H:\\CovInDB\\code\\CovInDB\\crawler\\2021\\pdbfile'

# select ligand, resn x
# cmd.select('ligand','byres 5UEH within 6 of resn GOL resn 85P')
def autoshow(i,distance = 6):
    p = Path(path)
    file = p.joinpath(f"{i}.pdb")
    cmd.load(file,i)
    cmd.remove('solvent')
    mole = moleculeidentity(f"{i}",path)
    rawstring = 'resn ' + ' resn '.join(mole.ligIdNoion)
    cmd.select('ligand',f'{rawstring} around 6') # 选择一个在当前pdb对象中配体残基周围距离为6A的口袋对象
    # cmd.create('pocket',f'byres {i} within {distance} of {rawstring}') # 创建一个在当前pdb对象中配体残基周围距离为6A的口袋对象
    cmd.show('lines','ligand ') # 在distance距离内显示侧链
    # cmd.reinitialize()
    return mole.ligIdNoion

# error class
class PathError(BaseException):
    def __init__(self,arg):
        self.arg = arg

class moleculeidentity():
    """moleculeidentity [summary]

    [识别pdb蛋白文件中的小分子标识符]
    """

    def __init__(self,pdbfile,path=path):
        self.pathstr = path
        self.path = Path(path)
        self.pdbfile = pdbfile
        self._init()

    def _init(self):
        if not self.path.exists():
            raise PathError('path not exist')
        if not isinstance(self.pdbfile,str):
            raise TypeError('Pdbid must be a string!')
        if ('.pdb' not in self.pdbfile) and (len(self.pdbfile) != 4):
            raise TypeError('Pdbid must be 4 letters')
        if ('.pdb' or '.PDB') in self.pdbfile:
            raise TypeError(f'{self.pdbfile} Remove ".pdb" from input arg, add automatically')
        file_list =  list(self.path.glob('*.pdb'))
        self.path_parent = file_list[0].parent
        self.pdbfilelist = [i.name[:4].upper() for i in file_list]

    def __parse_pdb_ligid(self,ion=True):
        if self.pdbfile.upper() not in self.pdbfilelist:
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
        # return ligId include ion
        return self.__parse_pdb_ligid()

    @property
    def ligIdNoion(self):
        return self.__parse_pdb_ligid(ion=False)

    @staticmethod
    def check_line_header(line_text):
        return line_text[0:6].strip()
            
    def __generate_pdb_lines(self):
        openpdbfile = self.pdbfile + '.pdb' if '.pdb' not in self.pdbfile else self.pdbfile
        for row in open(self.path_parent.joinpath(openpdbfile),'r+'):
            yield row.strip()




