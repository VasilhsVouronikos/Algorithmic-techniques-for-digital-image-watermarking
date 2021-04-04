import sys
import os


def update():
	unimported_pack = []
	with open(os.getcwd()+"/required_packages.txt","r") as req:
		data = req.readlines()
		for d in data:
			if(d.find("imported") < 0):
				unimported_pack.append(d)
				print("package " + (d.strip("\n").split("=")[1]) + " ready to install")
			else:
				print("deleting allready installed package " + (d.split("=")[1].split(" ")[0]))	

	with open(os.getcwd()+"/required_packages.txt","w+") as req:
		req.writelines(unimported_pack)


update()	
