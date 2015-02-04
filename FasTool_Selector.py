#=== FasTool_Selecter ===
#How to use
#
#
#Fasta and Qual Files => FastaQ File and List of nonmatched Fasta/Qual names
#
#Multiple Fasta Files => Marged Fasta File
#Multiple Qual Files => Marged Qual File
#Multiple FastaQ Files => Marged FastaQ File
#
#Fasta and Convert Files => Converted Fasta File
#Qual and Convert Files => Converted Qual File
#FastaQ and Convert Files => Converted FastaQ File
#
import re
import sys
import os

try:
	#define object for fasta data
	class FastaData:
		def __init__(self,name,data):
			self.name=name
			self.data=data
		def toFastQ(self,Qual):
			QualList=re.split(r"\s+",Qual.qual)
			asciiQual="".join(list(map(lambda x: chr(int(x)+33),QualList)))
			return FastQData(self.name,self.data,asciiQual)	
		def size(self):
			return len(self.data)
	class QualData:
		def __init__(self,name,qual):
			self.name=name
			self.qual=qual	
		def size(self):
			return len(re.split(r"\s+",self.qual))
	class FastQData:
		def __init__(self,name,data,qual):
			self.name=name
			self.data=data
			self.qual=qual
		def toFasta(self):
			return FastaData(self.name,self.data)
		def toQual(self):
			numQual=" ".join(map(lambda x: str(ord(x)-33), list(self.qual)))
			return QualData(self.name,numQual)
		def size(self):
			return len(self.data)

	#read fasta/qual  file
	def readFastaFile(FileName, IsQual=0):
		File=open(FileName, mode='r')
		
		FastaList=[]

		IsName=0
		Name=""
		Data=""

		regexIsDataName=re.compile(r"^>(.+)$",re.I)

		for Line in File:
			#erase CR and/or LF
			Line=Line.rstrip()

			#check whether the line is for a name of fasta
			if regexIsDataName.match(Line):
				#Add a previous data into the FastaList if we have
				if IsName and len(Data)>0:	
					if IsQual:	
						FastaList.append(QualData(Name,Data))
					else:
						FastaList.append(FastaData(Name,Data))
					#reset logs
					Name=""
					Data=""
					IsName=0

				#Get name of the fasta data and check the legnth of the name
				#	We will ignore this data if the name is empty
				Name=Line[1:]
				IsName=(len(Name)>0)
			else:
				#Get data
				#	Marge all data in multiple lines into a single data as long as no name line is read.
				Data+=Line

		#Add the last data into the FastaList if we have
		if IsName and len(Data)>0:				
			if IsQual:	
				FastaList.append(QualData(Name,Data))
			else:
				FastaList.append(FastaData(Name,Data))

		File.close()

		return FastaList
	#write fasta/qual file
	def writeFastaFile(FileName, Data, IsQual=0):
		File=open(FileName, mode='w')
		for Datum in Data:
			File.write(">"+Datum.name+"\n")
			if IsQual:
				File.write(Datum.qual+"\n")
			else:
				File.write(Datum.data+"\n")
		File.close()
	#read fastq file from File object
	def readFastQFile(FileName):
		File=open(FileName, mode='r')

		FastQList=[]

		Mode=0	#0:WaitName, 1:WaitData, 2:WaitQual
		Name=""
		Data=""
		Qual=""

		regexIsDataName=re.compile(r"^@(.+)$",re.I)
		regexIsQualBegin=re.compile(r"^\+",re.I)

		for Line in File:
			#erase CR and/or LF
			Line=Line.rstrip()

			#check whether the line is for a name of fasta
			if regexIsDataName.match(Line):
				#Add a previous data into the FastQList if we have
				if Mode>0 and len(Data)>0:
					FastQList.append(FastQData(Name,Data,Qual))
					#reset logs
					Name=""
					Data=""
					Qual=""
					Mode=0

				#Get name of the fasta data and check the legnth of the name
				#	We will ignore this data if the name is empty
				Name=Line[1:]
				if len(Name)>0:
					Mode=1
			else:
				if Mode==1 and regexIsQualBegin.match(Line):
					Mode=2
					continue
				
				if Mode==1:
					Data+=Line
				elif Mode==2:
					Qual+=Line

		#Add a previous data into the FastQList if we have
		if Mode>0 and len(Data)>0:	
			FastQList.append(FastQData(Name,Data,Qual))

		File.close()
		
		return FastQList
	#write fastq file
	def writeFastQFile(FileName, Data):
		File=open(FileName, mode='w')
		for Datum in Data:
			File.write("@"+Datum.name+"\n")
			File.write(Datum.data+"\n")
			File.write("+\n")
			File.write(Datum.qual+"\n")			
		File.close()
	#marge fasta and qual
	def margeFastaQual(FDataList,QDataList):
		FQDataList=[]
		for FData in FDataList:
			for QData in QDataList:
				if(FData.name == QData.name):
					FQDataList.append(FData.toFastQ(QData))
					break
		return FQDataList

	#File Path Holder
	class FilePathHolder:
		def __init__(self,path,name,type):
			self.path=path
			self.name=name
			self.type=type
		def fullpath(self):
			return self.path+self.name+"."+self.type
	#Command Holder
	class CommandData:
		def __init__(self, code, arg1, arg2):
			self.code=code
			self.arg1=arg1
			self.arg2=arg2
	#read Selection File
	def readSelFile(FileName):
		File=open(FileName, mode='r')
		
		CommandList=[]

		regexIsCode=re.compile(r"^__(.+)__(.*)",re.I)

		for Line in File:
			#erase CR and/or LF
			Line=Line.rstrip()
			
			if len(Line)==0:
				continue

			#check whether the line is for a name of fasta
			matchIsCode=regexIsCode.match(Line)
			if matchIsCode:
				Code=matchIsCode.group(1)
				CodeArgs=matchIsCode.group(2).split("\t")
			else:
				Code=""
				CodeArgs=Line.split("\t")
				
			if len(CodeArgs)>=2:
				Arg1=CodeArgs[0]
				Arg2=CodeArgs[1]
			elif len(CodeArgs)==1:
				Arg1=CodeArgs[0]
				Arg2=""
			else:
				Arg1=""
				Arg2=""
				
			CommandList.append(CommandData(Code,Arg1,Arg2))

		File.close()

		return CommandList
		
		
	#make regex for getting full file name from file path.
	regexFullFileName=re.compile(r"(.+)([/\\])([^/\\]+)$",re.I)	
	#make regex for separate file name and file extension from full file name.
	regexSeparateFileName=re.compile(r"(.+)\.([^\.]+?)$",re.I)

	#read arguments and erase own file path.
	Args = sys.argv
	Args.pop(0)
	#read all files in arguments
	IsMessage=0
	FileList=[]
	SelFileList=[]
	for Arg in Args:
		#read FullFileName from Arg
		MatchFullFileName=regexFullFileName.search(Arg)
		if not MatchFullFileName:
			print("********* ERROR *********\n> fail to find this file.")
			print("> Path: "+Arg+"\n")
			IsMessage=1
			continue
		
		FilePath=MatchFullFileName.group(1)+MatchFullFileName.group(2)
		
		#separate FileName from file type name
		MatchFileName=regexSeparateFileName.match(MatchFullFileName.group(3))
		if not MatchFileName:
			print("********* ERROR *********\n> fail to find file type.")
			print("> Path: "+Arg+"\n")
			IsMessage=1
			continue
		
		#get filename and extension
		FileName=MatchFileName.group(1)
		FileType=MatchFileName.group(2)
		
		if FileType == "fastq" or FileType == "fasta" or FileType == "fas" or FileType == "qual":
			FileList.append(FilePathHolder(FilePath,FileName,FileType))
		elif FileType == "txt":
			SelFileList.append(FilePathHolder(FilePath,FileName,FileType))
		else:
			print("********* WARNING *********\n> unexpected file type.")
			print("> multiple qual files with same name are detected.\n")
			IsMessage=1
			continue

	for File in FileList:
		Data=[]
		if File.type == "fastq":
			Data=readFastQFile(File.fullpath())
		elif File.type == "fasta" or File.type == "fas":
			Data=readFastaFile(File.fullpath(),0)
		elif File.type == "qual":
			Data=readFastaFile(File.fullpath(),1)
		else:
			continue

		#Make Dictionary {Name:Data}
		OriginalDict=dict()
		for Datum in Data:
			OriginalDict.update({Datum.name:Datum})

		#Read Each Command Files
		for SelFile in SelFileList:			
			CommandList=readSelFile(SelFile.fullpath())
			
			AnsData=[]
			Result=[]
			Dict=OriginalDict

			#Read Each CommandLine
			for Command in CommandList:
				print(Command.code+":"+Command.arg1+","+Command.arg2)
				
				#Simple Name Select 
				if Command.code == "":
					if Command.arg1 in Dict:
						AnsDatum = Dict[Command.arg1]
						#Rename Case
						if Command.arg2 != "":
							AnsDatum.name=Command.arg2
						AnsData.append(AnsDatum)
					else:
						Result.append("Fail to Find: "+Command.arg1+"\t"+Command.arg2)
				#Regex Name Select
#				elif Command.code == "NAME":
#					if len(Command.arg1)>0:
#						regexCommand=re.compile(Command.arg1)
#					
#					PreSize = len(Dict)
#					for Key in Dict.keys():
#						if not regexCommand.match(Key):
#							del Diect[Key]
#						
#				elif Command.code == "SIZE":
				else:
					Result.append("Unknown Code: "+Command.code+"\t"+Command.arg1+"\t"+Command.arg2)		
					
			if len(AnsData)>0:
				if File.type == "fastq":
					Data=writeFastQFile(File.path+File.name+"."+SelFile.name+"."+File.type,AnsData)
				elif File.type == "fasta" or File.type == "fas":
					Data=writeFastaFile(File.path+File.name+"."+SelFile.name+"."+File.type,AnsData,0)
				elif File.type == "qual":
					Data=writeFastaFile(File.path+File.name+"."+SelFile.name+"."+File.type,AnsData,1)
				else:
					continue
					
			if len(Result)>0:
				Fout=open(File.path+File.name+"."+SelFile.name+".log","w")
				for EachResult in Result:
					Fout.write(EachResult+"\n")
				Fout.close()
except:
	print("********* ERROR *********\n> Unexpected error:"+sys.exc_info()[0])
	IsMessage=1
finally:
	if IsMessage:
		os.system("pause")
		sys.exit()
