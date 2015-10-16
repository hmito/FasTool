# FasTool
## Aim
One of common file formats for the genetic sequence data is fasta format.
The aim of this project is to provide simple python programs which are helpful for managing fasta files.

## How to use
You can use the following files just by launching by python with some run-time arguments.
If you have not installed Python 3.x in your computer, please download at the website and install it.
https://www.python.org/

If you are using Windows machine, most simple way to use FasTool files are drag and drop target files on the Fastool files.

Othewise, you can use Fastool from terminal (console) as the following.
```
python [File path of FasTool] [Target File Path]
```
For example, if you want to use FasTool_FastaQualConverter.py for foo.fastq, change your current path to the directory where both FasTool_FastaQualConverter.py and foo.fastq exist, and type as the folloiwng.
```
python FasTool_FastaQualConverter.py foo.fastq
```

## FasTool_FastaQualConverter.py
FastaQualConverter can converte between fastq file and fasta/qual files.
If you input foo.fastq file, foo.fasta and foo.qual are created at the same directory with foo.fastq.
Similarly, if you input bar.fasta and bar.qual files, bar.fastq file is created. Please note that the conversion from fasta/qual files to fastq file will be carried out only when both file names of fasta and qual are same.

You can input multiple files simultaniously. In such case, FastaQualConverter will output all convertable files from input files.

## FasTool_Selector.py
FasTool_Selector can pick up some data from fasta/qual/fastq files.
For using this program, first you should make a txt file written the list of tha names of sequence data.
If you input the text file and fasta/qual/fastq files, the sequence data whose name is written in the list will be picked up.

For example, let's consider a foo.fasta, which is like the folloing.
```
>Seq1
ATATGAATCTTTT
>Seq2
ATATGAAACTTT
>Seq3
ATATGTTACTTTT
>Seq4
ATATGAACTTTT
```
Let's make bar.txt like the following.
```
Seq1
Seq3
```
Then, if you input foo.fasta and bar.txt simultaniously into Selector, Selector will be output foo.bar.fasta, which will be written as
```
>Seq1
ATATGAATCTTTT
>Seq3
ATATGTTACTTTT
```

#The MIT License (MIT)

Copyright (c) 2015 Koichi Ito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
