#argument: gb file name
#return: table file
read.gdfile_country_host_iso = function(gbfilename){
	fin  <- file(gbfilename, open = "r")

	cnt = 1
	Table = NULL
	Line = list(accession=NULL,contry=NULL, host=NULL, isolation_source=NULL, origin=NULL)
	origin_mode = FALSE
	
	#read each line
	while (length(str <- readLines(fin, n = 1, warn = FALSE)) > 0) {
		#at origin sections
		if(origin_mode){
			if(length(grep("^[0-9A-Za-z/]",str))>0){
				origin_mode=FALSE
			}else{
				Line$origin = paste0(Line$origin,gsub("[^a-zA-Z]", "", str))
			}
		}
			
		#at other sections
		if(!origin_mode){
			if(length(grep("ACCESSION",str))>0){
				Line$accession = sub("^ACCESSION\\s+([^\\s]+)$","\\1",str)
			}else if(length(grep("/country=",str))>0){
				Line$contry = sub(".*/country=\"(.+)\".*","\\1",str)
			}else if(length(grep("/host=",str))>0){
				Line$host = sub(".*/host=\"(.+)\".*","\\1",str)
			}else if(length(grep("/isolation_source=",str))>0){
				Line$isolation_source = sub(".*/isolation_source=\"(.+)\".*","\\1",str)
			}else if(length(grep("^//",str))>0){
				origin_mode = FALSE
				Table = rbind(Table, Line)
				Line = list(accession=NULL,contry=NULL, host=NULL, isolation_source=NULL, origin=NULL)
			}else if(length(grep("^ORIGIN",str))>0){
				origin_mode = TRUE
			}
		}
	}
	if(!is.null(Line$accession)){
		Table = rbind(Table, Line) 
	}
	
	close(fin)
	
	#remove line names
	rownames(Table) = NULL
	
	return(Table)
}

#example
gbfilename = "sequence-5.gb"
ans = read.gdfile_country_host_iso("sequence-5.gb")
