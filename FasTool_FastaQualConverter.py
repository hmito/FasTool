#=== FasTool_FastaQualConverter ===
#How to use
#	input Fasta and Qual Files 
#	=> output FastQ File
#	input FastQ File 
#	=> output Separate Fasta and Qual Files

import re
import sys
import os

#define object for fasta data
class FastaData:
	def __init__(self,name,data):
		self.name=name
		self.data=data
	def toFastQ(self,Qual):
		QualList=re.split(r"\s+",Qual.qual)
		asciiQual="".join(list(map(lambda x: chr(int(x)+33),QualList)))
		return FastQData(self.name,self.data,asciiQual)	
class QualData:
	def __init__(self,name,qual):
		self.name=name
		self.qual=qual	
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

#make regex for getting full file name from file path.
regexFullFileName=re.compile(r"[^/\\]+$",re.I)	
#make regex for separate file name and file extension from full file name.
regexSeparateFileName=re.compile(r"(.+)\.([^\.]+?)$",re.I)

#read arguments and erase own file path.
Args = sys.argv
Args.pop(0)

#DataBuffer
fastaDataList=[]
qualDataList=[]
fastQDataList=[]
commandData=[]

#read all files in arguments
FQFileName=""
for Arg in Args:
	print(Arg)

	#read FullFileName from Arg
	MatchFullFileName=regexFullFileName.search(Arg)
	if not MatchFullFileName:
		print("********* ERROR *********\n> fail to find this file.")
		os.system("pause")
		sys.exit()
	
	
	#separate FileName from file type name
	MatchFileName=regexSeparateFileName.match(Arg,MatchFullFileName.start(),MatchFullFileName.end())
	if not MatchFileName:
		print("********* ERROR *********\n> fail to find file type.")
		os.system("pause")
		sys.exit()
	
	#get filename and extension
	FileName=MatchFileName.group(1)
	FileType=MatchFileName.group(2)
	
	print("\tFileName: "+FileName);
	print("\tFileType: "+FileType);

	if FileType == "fasta" or FileType == "fas":
		if len(FQFileName) == 0:
			FQFileName = FileName + ".fq.fastq"
		Data=readFastaFile(Arg,0)
		print("\tNum: "+str(len(Data)))
		fastaDataList.extend(Data)

	elif FileType == "qual":
		Data=readFastaFile(Arg,1)
		print("\tNum: "+str(len(Data)))
		qualDataList.extend(Data)

	elif FileType == "fastq":
		Data=readFastQFile(Arg)
		print("\tNum: "+str(len(Data)))
		
		fData=list(map(lambda x:x.toFasta(),Data))
		qData=list(map(lambda x:x.toQual(),Data))
		
		writeFastaFile(FileName+"."+FileType+".fasta",fData,0)
		writeFastaFile(FileName+"."+FileType+".qual",qData,1)

	else:
		print("********* ERROR *********\n> fail to detect file type.")
		print("> Only fasta, fas, qual, fastq or txt files can be accepted.")
		os.system("pause")
		sys.exit()
	
if len(fastaDataList)>0 and len(qualDataList)>0:
	fqDataList=[]
	for fData in fastaDataList:
		for qData in qualDataList:
			if(fData.name == qData.name):
				fqDataList.append(fData.toFastQ(qData))
				break

	writeFastQFile(FQFileName,fqDataList)
				
	if len(fqDataList) != len(fastaDataList) or len(fqDataList) != len(qualDataList):
		print("********* WARNING *********\n> Some fasta/qual data are not matched.")
		print("Fasta: "+str(len(fastaDataList)))
		print("Qual : "+str(len(qualDataList)))
		print("FastQ: "+str(len(fqDataList)))
		os.system("pause")
		sys.exit()
