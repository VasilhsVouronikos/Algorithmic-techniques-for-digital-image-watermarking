import subprocess
import sys,os
import pip

def get_required_packages():
	if(sys.platform == "linux" or sys.platform == "Linux"):
		with open(os.getcwd()+"/required_packages.txt","r") as req:
			modules = []
			for lines in req:
				line = lines.strip("\n").split("=")
				d_lines = line[1].split(" ")
				if(len(d_lines) <= 1):        # module marked as imported
					modules.append(line[1])
				else:
					print("module " + d_lines[0] + " allready installed")
	else:
		with open(os.getcwd()+"\\required_packages.txt","r") as req:
			modules = []
			for lines in req:
				line = lines.strip("\n").split("=")
				d_lines = line[1].split(" ")
				if(len(d_lines) <= 1):        # module marked as imported
					modules.append(line[1])
				else:
					print("module " + d_lines[0] + " allready installed")

	return modules

def install_package():
	packages = get_required_packages()
	i = 0
	data = None
	with open(os.getcwd()+"/required_packages.txt","r") as req:
		data = req.readlines()
	for pack in packages:
		try :
			import pack
		except:
			res = subprocess.run(["pip3", "install",pack])

	return data
 

def update_state(data):
	updated_data = []
	for d in data:
		if(d.find("imported") < 0):
			updated_data.append((d.strip("\n") + " " + "imported\n"))
		else:
			updated_data.append(d)

	with open(os.getcwd()+"/required_packages.txt","w+") as req:
		req.writelines(updated_data)

print("Installing packages ...")
packages = install_package()
update_state(packages)
print("Done!!")