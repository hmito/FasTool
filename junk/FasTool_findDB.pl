#********** �ݒ荀�� 1 *********#
#�f�[�^�x�[�X�t���p�X�����炩���ߋL��
$DBFile[0]="C:\\Users\\k-ito\\Desktop\\database_ect.gb";
#*******************************#

#**********�ݒ荀�� 2 **********#
#ORGANISM�̍��ŒT�������L�[���[�h���L��
#$SearchSpecies[0]="Russula";
#$SearchSpecies[1]="Boletus";
#*******************************#

#**********�ݒ荀�� 3 **********#
#TITLE�̍��ŒT�������L�[���[�h���L��
$SearchTitle[0]="ectomycorrhiza";
#*******************************#

open(SearchSP,"<SearchSpecies.txt");
while($Line=<SearchSP>){
	chomp($Line);
	@SearchSpecies=(@SearchSpecies,$Line);
}
close(SearchSP);

open(SearchTITLE,"<SearchTitle.txt");
while($Line=<SearchTITLE>){
	chomp($Line);
	@SearchSpecies=(@SearchSpecies,$Line);
}
close(SearchTITLE);

foreach $EachDBFile(@DBFile){
	
	print("read database $EachDBFile\n");
	
	#�f�[�^�x�[�X���[�h
	open(DBFILE,"<".$EachDBFile);
	
	$CntDataNum=0;
	#��ɐ^
	while(1){
		#������
		@DBLineList=undef;
			
		#�t�@�C���̏I�[�܂ōs���Ă���ꍇ
		unless($DBLineList[0]=<DBFILE>){
			last;
		}

		#��s���f�[�^�x�[�X���[�h
		$IsLargeData=0;
		while($DBLine=<DBFILE>){
			if($DBLine=~m/\/\//){
				last;
			}
			if(@DBLineList<1000){
				@DBLineList=(@DBLineList,$DBLine);
			}elsif(@DBLineList==1000){
				$IsLargeData=1;
			}
		}
		if($IsLargeData==1){
			next;
		}
		
		#�ǂ�ł���s�𐧌䂷��
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#ACCESSION�̍���AcsNo�Ɋ��S�Ɉ�v���邩
			if($DBLine=~/^ACCESSION\s+(.*)$/){
				$isOK=1;
				$AcsNo=$1;
			}
		}
		#�����Ɏ��s���Ă���Ύ���
		if($isOK==0){
			next;
		}
		
		#�ǂ�ł���s�𐧌䂷��
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#DEFINITION�����݂��邩
			if($isOK==0){
				if($DBLine=~/^DEFINITION +([^\n]+)/){
					#���ʂ��L�^
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#�X�y�[�X��12����΁A���̍s���L�^���Ă���
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#�t�@�C���ɏo��
		if($isOK==0){
			$Definition{$AcsNo}="fail";
		}else{
			$Definition{$AcsNo}=$tmpStr;
		}
		
		#�ǂ�ł���s�𐧌䂷��
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#^  ORGANISM�����݂��邩
			if($isOK==0){
				if($DBLine=~/^  ORGANISM +([^\n]+)/){
					#���ʂ��L�^
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#�X�y�[�X��12����΁A���̍s���L�^���Ă���
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#�t�@�C���ɏo��
		if($isOK==0){
			$Organism{$AcsNo}="fail";
		}else{
			$Organism{$AcsNo}=$tmpStr;
		}
		
		#�ǂ�ł���s�𐧌䂷��
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#^  TITLE�����݂��邩
			if($isOK==0){
				if($DBLine=~/^  TITLE +([^\n]+)/){
					#���ʂ��L�^
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#�X�y�[�X��12����΁A���̍s���L�^���Ă���
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#�t�@�C���ɏo��
		if($isOK==0){
			$Title{$AcsNo}="fail";
		}else{
			$Title{$AcsNo}=$tmpStr;
		}
		
		++$CntDataNum;
		
		if($CntDataNum%100==0){
			print("*");
			$old = select(STDOUT);
			$| = 1;
			select($old);
			if($CntDataNum%1000==0){
				print("\t$CntDataNum\n");
			}
		}
	}
	print("\t$CntDataNum\n");
	
	#DB�t�@�C�������
	close(DBFILE);
}


#�����̃t�@�C�������ɊJ��
foreach $InputFile(@ARGV){
	print("read csv $InputFile\n");

	open(FIN,"<".$InputFile);	#�t�@�C���I�[�v��
	@File=<FIN>;				#�S�s��ۑ�
	close(FIN);

	chomp(@File);	#���s�R�[�h�폜
	
	open(FOUT,">".$InputFile."result.csv");	#�����t�@�C�����������݂ŊJ��
	
	#�V���ȗ��ǉ�����(csv�t�@�C���ł��邱�Ƃ��O��)
	print FOUT ($File[0].",Accession,Definition");
	print FOUT (",Organism");
	foreach $EachSearchSpecies(@SearchSpecies){
		print FOUT (",\"$EachSearchSpecies\"");
	}
	
	print FOUT (",Title");
	foreach $EachSearchTitle(@SearchTitle){
		print FOUT (",\"$EachSearchTitle\"");
	}
	
	print FOUT ("\n");
	
	#�擪�f�[�^�폜
	shift(@File);
	
	#�e�s�̃f�[�^�ǂݍ���
	$CntLine=0;
	foreach $Line(@File){
		print("(".(++$CntLine)."/".(@File+0).") ");
		print FOUT ($Line);
		
		#AcsNo������Z����؂�o���i2�ڂ̃Z���j
		if($Line!~/[^,]+,([^,]+),/){
			print FOUT (",fail\n");
			next;
		}
		$AcsCell=$1;
		
		#AcsNo��؂�o���i4�ڂ̋�؂�j
		if($AcsCell!~/[^\|]+\|[^\|]+\|[^\|]+\|([^\|\.]+)/){
			print FOUT (",fail\n");
			next;
		}
		$AcsNo=$1;
		print FOUT (",$AcsNo");
		
		print FOUT (",\"$Definition{$AcsNo}\"");
		
		print FOUT (",\"$Organism{$AcsNo}\"");
		foreach $tmpSearch(@SearchSpecies){
			if($Organism{$AcsNo}=~/$tmpSearch/i){
				print FOUT (",1");
			}else{
				print FOUT (",0");
			}
		}
		
		print FOUT (",\"$Title{$AcsNo}\"");
		#���O�̏������m�F
		$IsSearch=0;
		foreach $tmpSearch(@SearchTitle){
			if($Title{$AcsNo}=~/$tmpSearch/i){
				print FOUT (",1");
			}else{
				print FOUT (",0");
			}
		}
		
		
		#DB�T���I��
		print("\n");
		print FOUT ("\n");
	}
	
	#�������ݏI��
	close(FOUT);	
}
