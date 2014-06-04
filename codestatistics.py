import os;

isContainAnnotate = False;
is_writefile = True;
out_file_name = "codestatistics.txt";

overcode_print_rule = 0;
basepath="";

#check str whether is annotate
def isAnnotate(str, ext):
	if isContainAnnotate:
		return False;
	flag = (cmp(str, "") == 0) or str.startswith("\/") or \
			str.startswith("*");
	if(cmp(ext, ".py") == 0 or cmp(ext, ".sh") == 0):
		flag = flag or str.startswith("#");
	elif(cmp(ext, ".xml") == 0):
		flag = flag or str.startswith("<!--");
	elif(cmp(ext, ".bat") == 0):
		flag = flag or str.startswith("rem");	
	return flag;

#calculate file line count
def calculatelinecount(path):
	basepath, ext = os.path.splitext(path);
	fp = file(path);
	lines = fp.readlines();
	count = 0;
	for item in lines:
		item = item.lstrip();
		item = item.rstrip();
		if (not isAnnotate(item, ext)):
			count = count + 1;
	fp.close();
	return count;
	
def isPic(itempath):
	if itempath.endswith(".png") or itempath.endswith(".bmp") or \
		itempath.endswith(".gif") or itempath.endswith(".jpeg") or \
		itempath.endswith(".jpg"):
		return True;
	else:
		return False;

def isMusic(itempath):
	if itempath.endswith(".mp3") or itempath.endswith(".mp4") or \
		itempath.endswith(".wma") or itempath.endswith(".wav") or \
		itempath.endswith(".wmv") or itempath.endswith(".mid") or \
		itempath.endswith(".rm"):
		return True;
	else:
		return False;

def isVideo(itempath):
	if itempath.endswith(".mpeg") or itempath.endswith(".avi") or \
		itempath.endswith(".m3u8") or itempath.endswith(".f4v"):
		return True;
	else:
		return False;
		
def isComplineCode(itempath):
	if itempath.endswith(".class") or itempath.endswith(".o") or \
		itempath.endswith(".a") or itempath.endswith(".dll") or \
		itempath.endswith(".so") or itempath.endswith(".jar"):
		return True;
	else:
		return False;
	
#whether is correct file
def isFile(itempath):
	itempath = itempath.lower();
	if (os.path.isfile(itempath)) and \
		(not isComplineCode(itempath)) and \
		(not isMusic(itempath)) and \
		(not isVideo(itempath)) and \
		(not isPic(itempath)): 
		return True;
	else:
		return False;

#whether is correct folder
def isFolder(path, filename):
	if os.path.isdir(path) and \
		(cmp(filename, ".svn") != 0) and \
		(cmp(filename, ".settings") != 0) and \
		(cmp(filename, "debug") != 0) and \
		(cmp(filename, "release") != 0) and \
		(cmp(filename, "gen") != 0) and \
		(cmp(filename, "lib") != 0) and \
		(cmp(filename, "libs") != 0) and \
		(cmp(filename, "bin") != 0):
	   return True;
	else:
	   return False;

#add separator
def addSeparator(path):
	separator = "";
	if not path.endswith("\\"):
		separator = "\\";
	return separator;
	   
#file operation
class CodeFile:
	fp = -1;
	
	def open(self, path):
		if os.path.isdir(path) and is_writefile:
			path = path + addSeparator(path) + out_file_name;
			os.walk(path);
			self.fp = file(path, "w");
	   
	def write(self, message):
		if self.fp != -1:
			self.fp.write(message);
	   
	def close(self):
		if self.fp != -1:
			self.fp.close();

#format out
def formatStr(itemcount, size):
	format = str(itemcount);
	formatlen = size - len(format);
	i = 0;
	while i < formatlen:
		i = i + 1;
		format = format + " ";
	return format;
			
#print content
def printAndSaveMessage(itemcount, filesize, itempath, fo):
	if itempath.startswith("\\"):
		itempath = itempath[len("\\"):];
	if itemcount > overcode_print_rule:
		outStr = "linecount: %s  filesize(byte):%s  %s" \
			% (formatStr(itemcount, 5), formatStr(filesize, 7), itempath);
		fo.write(outStr + "\n");
		print outStr;

#listfiles
def listfiles(path, fo):
	linecount = 0;
	filecount = 0;
	if isFile(path):
		filecount = filecount + 1;
		size = os.path.getsize(path);
		itemcount = calculatelinecount(path);
		printAndSaveMessage(itemcount, size, path, fo); #print and save
		linecount = linecount + itemcount;
		result = {"linecount":linecount, 'filecount':filecount};
		return result;
		
	if not isFolder(path, ""):
		return "path is not a directory!";
		
	filelist = os.listdir(path);
	for item in filelist:
		if cmp(item, out_file_name) == 0:
			continue;
		itempath = path + addSeparator(path) + item;
		if isFile(itempath):
			filecount = filecount + 1;
			itemcount = calculatelinecount(itempath);
			size = os.path.getsize(itempath);
			relativepath = itempath[len(basepath):];
			printAndSaveMessage(itemcount, size, relativepath, fo); #print and save
			linecount = linecount + itemcount;
		elif isFolder(itempath, item): #folder
			resp = listfiles(itempath, fo);
			linecount = linecount + resp['linecount'];
			filecount = filecount + resp['filecount'];
	result = {"linecount":linecount, 'filecount':filecount};
	return result;

#main enter	
prompt = "-----------------------";
prompt = prompt * 2;
path = raw_input("please input project path: ");
basepath = path;
fo = CodeFile();
fo.open(path);
fo.write(prompt + "\n");
print prompt;
resp = listfiles(path, fo);
result = "project linecount:%d  |  filecount:%d\n" \
				% (resp['linecount'], resp['filecount']);
fo.write(prompt + "\n" + result);
fo.close();
print prompt, "\n", result;
