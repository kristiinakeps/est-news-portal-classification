library(readr)
library(dplyr)
library(purrr)


# mostly emoji removal
removeSpecialSymbols <- function(str_input) {
    new_str <- gsub("<[^>]+>","",str_input)
    new_str <- gsub("[«»|]","",new_str)
    return(new_str)
  }
  

cleanFileCreatorCSV2 <- function(input_file,headline_colname,content_colname){
  full_dataset = read.csv2(input_file,encoding= "UTF-8")
  headline_clean <- full_dataset[,headline_colname] %>% 
    map(removeSpecialSymbols)
  content_clean <- full_dataset[,content_colname] %>% 
    map(removeSpecialSymbols)
  full_dataset[,headline_colname] <- unlist(headline_clean)
  full_dataset[,content_colname] <- unlist(content_clean)
  return(full_dataset)
}

cleanFileCreatorCSV <- function(input_file,headline_colname,content_colname){
  full_dataset = read.csv(input_file,encoding= "UTF-8")
  headline_clean <- full_dataset[,headline_colname] %>% 
    map(removeSpecialSymbols)
  content_clean <- full_dataset[,content_colname] %>% 
    map(removeSpecialSymbols)
  full_dataset[,headline_colname] <- unlist(headline_clean)
  full_dataset[,content_colname] <- unlist(content_clean)
  return(full_dataset)
}

del_rchange <- function(str_input){
  gsub("\r\n","",str_input)
}


clean_rowchange <- function(dataset,content_colname){
  content_clean <- dataset[,content_colname] %>% 
    map(del_rchange)
  dataset[,content_colname] <- unlist(content_clean)
  return(dataset)
}


postimees_clean <- cleanFileCreatorCSV2("postimees_final_new.csv","pealkiri","sisu")
write.csv2(postimees_clean,"postimees_cleaned.csv",fileEncoding = "UTF-8")

elu24_clean <- cleanFileCreatorCSV2("elu24_final_new.csv","pealkirjade_list","sisu")
write.csv2(elu24_clean,"elu24_cleaned.csv",fileEncoding = "UTF-8")



postimees_clean_s <- cleanFileCreatorCSV2("postimees_samples.csv","pealkiri","sisu")
write.csv2(postimees_clean_s,"postimees_samples_cleaned.csv",fileEncoding = "UTF-8")

elu24_clean_s <- cleanFileCreatorCSV2("elu24_samples.csv","pealkirjade_list","sisu")
write.csv2(elu24_clean_s,"elu24_samples_cleaned.csv",fileEncoding = "UTF-8")

paevaleht <- read_csv("paevaleht.csv",locale = readr::locale(encoding = "UTF-8"))
paevaleht_clean <- clean_rowchange(paevaleht,"sisu")
write.csv2(paevaleht_clean,"paevaleht_cleaned.csv",fileEncoding = "UTF-8")


err <- read_csv("err.csv",locale = readr::locale(encoding = "UTF-8"))
err_clean <- clean_rowchange(err,"article")
write.csv2(err_clean,"err_cleaned.csv",fileEncoding = "UTF-8")


telegram <- read_csv("telegram.csv",locale = readr::locale(encoding = "UTF-8"))
telegram_clean <- clean_rowchange(telegram,"sisu")
write.csv2(telegram_clean,"telegram_cleaned.csv",fileEncoding = "UTF-8")

uued_uudised <- read_csv("uued_uudised.csv",locale = readr::locale(encoding = "UTF-8"))
uued_uudised_clean <- clean_rowchange(uued_uudised,"sisu")
write.csv2(uued_uudised_clean,"uued_uudised_cleaned.csv",fileEncoding = "UTF-8")


ohtuleht <- read_csv("articles_ohtuleht_uus.csv",locale = readr::locale(encoding = "UTF-8"))
ohtuleht_clean <- clean_rowchange(ohtuleht,"article")
write.csv2(ohtuleht_clean,"ohtuleht_cleaned.csv",fileEncoding = "UTF-8")
