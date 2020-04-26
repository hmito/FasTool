#argument: gb file name
#return: table file
read.gdfile_country_host_iso = function(gbfilename){
	fin  <- file(gbfilename, open = "r")

	cnt = 1
	Table = NULL
	Line = data.frame(accession="",country="", host="", isolation_source="", origin="")
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
				if(length(grep(".*/country=\"(.+)\".*",str))>0){
					#single line case
					Line$country = sub(".*/country=\"(.+)\".*","\\1",str)
				}else{
					Spaces = sub("(.*)/country=.*","\\1",str)
					Line$country = sub(".*/country=\"(.+)$","\\1",str)
					while (length(str <- readLines(fin, n = 1, warn = FALSE)) > 0){
						str = sub(Spaces,"",str)
						if(length(grep("\"",str))>0){
							Line$country = paste0(Line$country," ",sub("(.*)\".*$","\\1",str))
							break
						}
						Line$country = paste0(Line$country, " ",str)
					}
				}
			}else if(length(grep("/host=",str))>0){
				if(length(grep(".*/host=\"(.+)\".*",str))>0){
					#single line case
					Line$host = sub(".*/host=\"(.+)\".*","\\1",str)
				}else{
					Spaces = sub("(.*)/host=.*","\\1",str)
					Line$host = sub(".*/host=\"(.+)$","\\1",str)
					while (length(str <- readLines(fin, n = 1, warn = FALSE)) > 0){
						str = sub(Spaces,"",str)
						if(length(grep("\"",str))>0){
							Line$host = paste0(Line$host," ",sub("(.*)\".*$","\\1",str))
							break
						}
						Line$host = paste0(Line$host, " ",str)
					}
				}
			}else if(length(grep("/isolation_source=",str))>0){
				if(length(grep(".*/isolation_source=\"(.+)\".*",str))>0){
					#single line case
					Line$isolation_source = sub(".*/isolation_source=\"(.+)\".*","\\1",str)
				}else{
					Spaces = sub("(.*)/isolation_source=.*","\\1",str)
					Line$isolation_source = sub(".*/isolation_source=\"(.+)$","\\1",str)
					while (length(str <- readLines(fin, n = 1, warn = FALSE)) > 0){
						str = sub(Spaces,"",str)
						if(length(grep("\"",str))>0){
							Line$isolation_source = paste0(Line$isolation_source," ",sub("(.*)\".*$","\\1",str))
							break
						}
						Line$isolation_source = paste0(Line$isolation_source," ", str)
					}
				}
			}else if(length(grep("^//",str))>0){
				origin_mode = FALSE
				Table = rbind(Table, Line)
				Line = data.frame(accession="",country="", host="", isolation_source="", origin="")
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
	
	return(data.frame(Table))
}

#example
gbfilename = "Cenococcum.gb"
ans = read.gdfile_country_host_iso(gbfilename)
