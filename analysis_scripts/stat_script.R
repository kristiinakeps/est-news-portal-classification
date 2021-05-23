library(stringi)
library(tidyverse)

extract_date <- function(date_string){
  extr_date_position <- regexpr("[0-9][0-9]:[0-9][0-9]",date_string)
  date <- substr(date_string,extr_date_position,extr_date_position+5)
  return(date)
}

mean_t_lens <<- c()
mean_t_count <<- c()
median_t_lens <<- c()
mean_c_count <<- c()
mean_c_lens <<- c()
median_c_lens <<- c()

create_statistics <- function(dataset,headline_colname,content_colname,column_colname,date_colname){
  dataset_prefix = deparse(substitute(dataset))
  title <- dataset[,headline_colname]
  title <- gsub("[\r\n]", "",title)
  title_data <- map(title,stringi::stri_stats_latex)
  unlist_title_data <- unlist(title_data)
  words_t_data <- unlist_title_data[grepl("Words",names(unlist_title_data))]
  chars_t_data <- unlist_title_data[grepl("CharsWord",names(unlist_title_data))]
  mean_t_lens <<- c(mean_t_lens,mean(chars_t_data))
  median_t_lens <<- c(median_t_lens,median(chars_t_data))
  mean_t_count <<- c(mean_t_count,mean(words_t_data))
  content <- dataset[,content_colname] 
  content <- gsub("[\r\n]", "",content)
  content_data <- map(content,stringi::stri_stats_latex)
  unlist_cont_data <- unlist(content_data)
  words_c_data <- unlist_cont_data[grepl("Words",names(unlist_cont_data))]
  chars_c_data <- unlist_cont_data[grepl("CharsWord",names(unlist_cont_data))]
  mean_c_lens <<- c(mean_c_lens,mean(chars_c_data))
  median_c_lens <<- c(median_c_lens,median(chars_c_data))
  mean_c_count <<- c(mean_c_count,mean(words_c_data))
  columns = table(dataset[,column_colname])
  if(dataset_prefix!="uued_uudised"){
    dates = map(dataset[,date_colname],extract_date)
    write.table(dates,paste(dataset_prefix,"_dates.txt",sep = ""), col.names=FALSE)
  }
  #write.csv(data.frame(title_data,content_data),paste(dataset_prefix,"_title_cont_lens.csv"))
  write.csv(columns,paste(dataset_prefix, "_columns.csv",sep = ""))
}

postimees_clean <- read.csv2("postimees_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(postimees_clean,"pealkiri","sisu","rubriik","kuupaev")

elu24_clean <- read.csv2("elu24_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(elu24_clean,"pealkirjade_list","sisu","rubriik_list","kuupaev_list")

paevaleht <- read.csv2("paevaleht_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(paevaleht,"pealkiri","sisu","teema","kpv")

err <- read.csv2("err_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(err,"header","article","tag","date")

ohtuleht <- read.csv2("ohtuleht_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(ohtuleht,"header","article","tags","date")

telegram <- read.csv2("telegram_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(telegram,"pealkiri","sisu","teema","kpv")

uued_uudised <- read.csv2("uued_uudised_cleaned.csv",fileEncoding = "UTF-8")
create_statistics(uued_uudised,"pealkiri","sisu","teema","kpv")

portals <- c("postimees","elu24","paevaleht","err","ohtuleht","telegram","uued_uudised")

len_dataframe <- data.frame(portals,mean_c_count,mean_c_lens,median_c_lens,mean_t_count,mean_t_lens,median_t_lens)



library("xlsx")

write.xlsx(len_dataframe, "len_data.xlsx", sheetName = "Sheet1", 
           col.names = TRUE, row.names = TRUE, append = FALSE)