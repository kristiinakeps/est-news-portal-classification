library(readr)
removeWords <- function(str, stopwords) {
  x <- unlist(strsplit(str, " "))
  paste(x[!x %in% stopwords], collapse = " ")
}

est_stopword_rem <- function(stopwords,input_file){
  full_string = read_file(input_file,locale = locale(encoding = "UTF-8"))
  full_string = tolower(full_string)
  no_stop <- removeWords(full_string,stopwords)
  return(no_stop)
}


sw <- read_table('est_fulls_sw.txt',col_names = F,locale = locale(encoding = "UTF-8"))


no_stop_telegram <- est_stopword_rem(sw$X1,'telegram.txt')
writeLines(no_stop_telegram, "no_stop_telegram.txt", useBytes=T)
no_stop_postimees <- est_stopword_rem(sw$X1,'postimees.txt')
writeLines(no_stop_postimees, "no_stop_postimees.txt", useBytes=T)
no_stop_elu24 <- est_stopword_rem(sw$X1,'elu24.txt')
writeLines(no_stop_elu24, "no_stop_elu24.txt", useBytes=T)
no_stop_paevaleht <- est_stopword_rem(sw$X1,'paevaleht.txt')
writeLines(no_stop_paevaleht, "no_stop_paevaleht.txt", useBytes=T)
no_stop_ohtuleht <- est_stopword_rem(sw$X1,'ohtuleht.txt')
writeLines(no_stop_ohtuleht, "no_stop_ohtuleht.txt", useBytes=T)
no_stop_err <- est_stopword_rem(sw$X1,'err.txt')
writeLines(no_stop_err, "no_stop_err.txt", useBytes=T)
no_stop_uued_uudised <- est_stopword_rem(sw$X1,'uued_uudised.txt')
writeLines(no_stop_uued_uudised, "no_stop_uued_uudised.txt", useBytes=T)
