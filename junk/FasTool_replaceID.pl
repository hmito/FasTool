foreach $InputFile(@ARGV){
	open(FIN,"<".$InputFile);
	open(FOUT,">".$InputFile."replace.fas");
	while($Str=<FIN>){
		if($Str=~/^>.*(cluster_[0-9]+)/){
			print FOUT (">$1\n");
		}else{
			print FOUT ($Str);
		}
	}
	close(FIN);
	close(FOUT);
}
