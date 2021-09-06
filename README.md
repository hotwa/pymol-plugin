# pymol共价键插件脚本



## 功能

### 概述

> 辅助查找pymol中pdb蛋白中共价键，最后一步需要人工查看

### 操作

> 通过pdb文件找到ligand，并在pymol中自动展示ligand周围6A（可以自己设置）内的lines

## 使用

进入家目录

window 为 C:\Users\user
linux cd ~
macos cd ~

复制`pymolrc.pml`和`pymol_plugin`至根目录。

在命令行环境中执行`pymol`自动打开软件，会自动加载autoshow函数

在pymol命令窗口执行autoshow命令，其中距离默认为**6A**，可以修改。也可以直接在`pymol_plugin.py`修改path变量

```python
path = '/yourpdbfiledir'
autoshow('pdbid',distance = 6,path)
```