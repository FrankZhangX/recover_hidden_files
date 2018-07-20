# -*- coding: utf-8 -*-

import os,shutil,time

ldname=[]			#初始盘符列表
#获得现有磁盘盘符
logicaldisk=list(os.popen('wmic logicaldisk get name'))
logicaldisk=logicaldisk[1:]
for i in logicaldisk:
	if i is not '\n':
		ldname.append(i[0])

#检测输入规范
while 1:
	try:
		disk=input('\n请输入已被隐藏病毒感染的磁盘盘符：\nPlease input the infected disk:  ')
	except Exception as e:
		print(e.reason)
	else:
		disk=disk.upper()
		if len(disk)==1 and ('A'<=disk<='Z'):
			if disk not in ldname:
				print('\n无该磁盘！\n')
				continue
			else:
				break
		else:
			print('\n输入不规范！只需输入盘符对应字母即可\n')
			continue
print('\n正在进行病毒查杀，请稍后......\n')
disk+=':\\'
pathlist=[disk]		#路径列表
filelist=[]			#文件列表
os.chdir(disk)
f=open('recover_log.txt','a')
f.writelines('查杀时间：'+time.strftime('%c',time.localtime())+'\n\n')

#列出目录结构
flag=0
f.writelines('---------原始文件目录结构---------------\n')
for (dirname,subdirs,files) in os.walk(pathlist[0]):
	if flag!=0:f.writelines('-------------------------\n')
	flag=1
	f.writelines('['+dirname+']\n')
	for fsub in subdirs:		#列出文件夹路径
		pathlist.append(os.path.join(dirname,fsub))
		f.writelines('[folder]:'+fsub+'\n')
	for fname in files:			#列出文件路径
		filelist.append(os.path.join(dirname,fname))
		f.writelines('[file]:'+fname+'\n')
f.writelines('--------------------------------\n\n')

#列出隐藏文件夹及文件
f.writelines('----------隐藏的文件夹----------------\n')
hide_d=0
for i in pathlist:
	a=list(os.popen('attrib '+i))
	if a[0][4]=='H':
		f.writelines(i+'\n')
		hide_d+=1
f.writelines('共'+str(hide_d)+'个隐藏文件夹\n\n')

f.writelines('----------隐藏的文件-----------------\n')
hide_f=0
for i in filelist:
	a=list(os.popen('attrib '+i))
	if a[0][4]=='H':
		f.writelines(i+'\n')
		hide_f+=1
f.writelines('共'+str(hide_f)+'个隐藏文件\n\n')

#开始修改文件夹及文件属性并删除exe病毒文件
os.popen('attrib -a -h -s -r /s /d')		#更改文件夹及文件属性
recover_d=[]		#恢复的文件夹
recover_f=[]		#恢复的文件
for (dirname,subdirs,files) in os.walk(pathlist[0]):
	for fsub in subdirs:
		recover_d.append(os.path.join(dirname,fsub))
	for fname in files:
		recover_f.append(os.path.join(dirname,fname))
f.writelines('\n----------查杀的exe病毒文件-------------\n')
exe_virue=0
for i in recover_f:		#找出变成exe的病毒文件
	extend=i[-3:]
	fname=i[:-4]
	if fname in recover_d and extend=='exe':
		print('\n正在查杀病毒文件',i,'\n')
		os.popen('del '+i)
		f.writelines(i+'\n')
		exe_virue+=1
f.writelines('共查杀'+str(exe_virue)+'个病毒文件')
f.writelines('\n-------------------------------\n')

f.close()

print('\n已完成病毒查杀\n')
print('\n查杀日志已写入查杀磁盘中，请在',disk,'recover_log.txt中查看\n',sep='')
print('\n本工具将在3秒后自动退出，感谢您的使用！\n')
time.sleep(3)