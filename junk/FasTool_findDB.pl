#********** 設定項目 1 *********#
#データベースフルパスをあらかじめ記入
$DBFile[0]="C:\\Users\\k-ito\\Desktop\\database_ect.gb";
#*******************************#

#**********設定項目 2 **********#
#ORGANISMの項で探したいキーワードを記入
#$SearchSpecies[0]="Russula";
#$SearchSpecies[1]="Boletus";
#*******************************#

#**********設定項目 3 **********#
#TITLEの項で探したいキーワードを記入
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
	
	#データベースロード
	open(DBFILE,"<".$EachDBFile);
	
	$CntDataNum=0;
	#常に真
	while(1){
		#初期化
		@DBLineList=undef;
			
		#ファイルの終端まで行っている場合
		unless($DBLineList[0]=<DBFILE>){
			last;
		}

		#一行ずつデータベースロード
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
		
		#読んでいる行を制御する
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#ACCESSIONの項でAcsNoに完全に一致するか
			if($DBLine=~/^ACCESSION\s+(.*)$/){
				$isOK=1;
				$AcsNo=$1;
			}
		}
		#発見に失敗していれば次へ
		if($isOK==0){
			next;
		}
		
		#読んでいる行を制御する
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#DEFINITIONが存在するか
			if($isOK==0){
				if($DBLine=~/^DEFINITION +([^\n]+)/){
					#結果を記録
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#スペースが12個あれば、次の行も記録しておく
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#ファイルに出力
		if($isOK==0){
			$Definition{$AcsNo}="fail";
		}else{
			$Definition{$AcsNo}=$tmpStr;
		}
		
		#読んでいる行を制御する
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#^  ORGANISMが存在するか
			if($isOK==0){
				if($DBLine=~/^  ORGANISM +([^\n]+)/){
					#結果を記録
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#スペースが12個あれば、次の行も記録しておく
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#ファイルに出力
		if($isOK==0){
			$Organism{$AcsNo}="fail";
		}else{
			$Organism{$AcsNo}=$tmpStr;
		}
		
		#読んでいる行を制御する
		$isOK=0;
		foreach $DBLine(@DBLineList){				
			#^  TITLEが存在するか
			if($isOK==0){
				if($DBLine=~/^  TITLE +([^\n]+)/){
					#結果を記録
					$tmpStr=$1;
					$isOK=1;
				}
			}else{
				#スペースが12個あれば、次の行も記録しておく
				if($DBLine=~/ {12}([^\n]+)/){
					$tmpStr=$tmpStr." ".$1;
				}else{
					last;
				}
			}
		}
		#ファイルに出力
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
	
	#DBファイルを閉じる
	close(DBFILE);
}


#引数のファイルを順に開く
foreach $InputFile(@ARGV){
	print("read csv $InputFile\n");

	open(FIN,"<".$InputFile);	#ファイルオープン
	@File=<FIN>;				#全行を保存
	close(FIN);

	chomp(@File);	#改行コード削除
	
	open(FOUT,">".$InputFile."result.csv");	#同名ファイルを書き込みで開く
	
	#新たな列を追加する(csvファイルであることが前提)
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
	
	#先頭データ削除
	shift(@File);
	
	#各行のデータ読み込み
	$CntLine=0;
	foreach $Line(@File){
		print("(".(++$CntLine)."/".(@File+0).") ");
		print FOUT ($Line);
		
		#AcsNoがあるセルを切り出す（2つ目のセル）
		if($Line!~/[^,]+,([^,]+),/){
			print FOUT (",fail\n");
			next;
		}
		$AcsCell=$1;
		
		#AcsNoを切り出す（4つ目の区切り）
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
		#名前の条件を確認
		$IsSearch=0;
		foreach $tmpSearch(@SearchTitle){
			if($Title{$AcsNo}=~/$tmpSearch/i){
				print FOUT (",1");
			}else{
				print FOUT (",0");
			}
		}
		
		
		#DB探索終了
		print("\n");
		print FOUT ("\n");
	}
	
	#書き込み終了
	close(FOUT);	
}
