#=== FasTool_FileConverter ===
#How to use
#
#Single Fasta File => nothing
#Single Qual File => nothing
#Single FastaQ File => Fasta + Qual Files
#
#Multiple Fasta Files => Marged Fasta File
#Multiple Qual Files => Marged Qual File
#Multiple FastaQ Files => Marged FastaQ File
#
#Fasta and Qual Files => FastaQ File and List of nonmatched Fasta/Qual names
#
#Fasta and Convert Files => Converted Fasta File
#Qual and Convert Files => Converted Qual File
#FastaQ and Convert Files => Converted FastaQ File
#
#Convert File
#	Name => Select the named Data 
#	$Expression => Select Data matching to the regular expression
#	$Expression1[\t]Expression2    Select Data matching to the regular expression1 and rename them with following the regular expression2
#

import re
import sys

#define object for fasta data
class FastaData:
	def __init__(self,name,data,qual):
		self.name=name
		self.data=data
		self.qual=qual

#read fasta file from File object
def read_fasta(File, IsQual=0):
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
					FastaList.append(FastaData(Name,"",Data))
				else:
					FastaList.append(FastaData(Name,Data,""))
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
			FastaList.append(FastaData(Name,"",Data))
		else:
			FastaList.append(FastaData(Name,Data,""))

	return FastaList

#read fastaq file from File object
def read_fastaq(file):
	return []

#make regex for getting full file name from file path.
regexFullFileName=re.compile(r"[^/\\]+?$",re.I)	
#make regex for separate file name and file extension from full file name.
regexSeparateFileName=re.compile(r"([^\.]+?)\.([^\.]+?)$",re.I)

#read arguments and erase own file path.
Args = sys.argv
Args.pop(0)

#DataBuffer
fastaData=[]
qualData=[]
fastaqData=[]

#read all files in arguments
for Arg in Args:
	print(Arg)

	#read FullFileName from Arg
	MatchFullFileName=regexFullFileName.search(Arg)
	if not MatchFullFileName:
		print("\t***Error*** fail to find this file.")
		continue
	
	
	#separate FileName from file type name
	MatchFileName=regexSeparateFileName.match(Arg,MatchFullFileName.start(),MatchFullFileName.end())
	if not MatchFileName:
		print("\t***Error*** fail to find file type.")
		continue
	
	#get filename and extension
	FileName=MatchFileName.group(1)
	FileType=MatchFileName.group(2)
	
	print("\tFileName: "+FileName);
	print("\tFileType: "+FileType);


	if FileType == "fasta" or FileType == "fas":
		Fin=open(Arg,mode='r')
		fastaData.append(read_fasta(Fin,0))
		Fin.close()

	elif FileType == "qual":
		Fin=open(Arg,mode='r')
		qualData.append(read_fasta(Fin,1))
		Fin.close()

	elif FileType == "fastaq":
		Fin=open(Arg,mode='r')
		fastaqData.append(read_fastaq(Fin))
		Fin.close()

	for Datum in fastaData:
		print(Datum.name)
		print(Datum.data)
		print("")