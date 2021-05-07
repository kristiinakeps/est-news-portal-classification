library(dplyr)
library(rvest)
library(readr)
library(stringr)

# ELU24
#
#
dates = c("NO","2020-11-17","2020-06-19","2020-01-27","2019-08-25","2019-03-13","2018-11-01")

# POSTIMEES
#
#
dates = c("NO","2021-02-27","2020-12-29","2020-10-30","2020-09-02","2020-06-27","2020-04-24")



pikkus = 0
pealkirjade_list = rep(NA,200000)
urls_list = rep(NA,200000)
rubriik_list = rep(NA,200000)
kuupaev_list = rep(NA,200000)

for (k in dates){
  print(k)
  if (k=="NO"){
    url_pre = 82
    #url = "https://www.postimees.ee/search?sections=80&fields=body%2Cauthors%2Cheadline&page=1"
    url = "https://www.postimees.ee/search?sections=81&fields=body%2Cauthors%2Cheadline&page=1"
  }else{
    url_pre = 160
    #url = paste("https://www.postimees.ee/search?start=2016-06-01T00%3A00%3A00%2B03%3A00&end=",k,"T23%3A59%3A59%2B02%3A00&sections=80&fields=body%2Cauthors%2Cheadline&page=1",sep = "")
    url = paste("https://www.postimees.ee/search?start=2016-06-01T00%3A00%3A00%2B03%3A00&end=",k,"T23%3A59%3A59%2B03%3A00&sections=81&fields=body%2Cauthors%2Cheadline&page=1",sep = "")
  }
  for (i in 1:997) {
    page = read_html(url)
    headline_nodes <- page %>% 
      html_nodes("a.article-content__headline") 
    pealkirjad <- headline_nodes %>% 
      html_text()
    urls <- headline_nodes %>% 
      html_attr('href')
    kuupaevad <- page %>% 
      html_nodes("span.article-content__date-published") %>% 
      html_text()
    rubriigid <- page %>% 
      html_nodes("a.article-content__section-name") %>% 
      html_text()
    pealkirjad <- str_split_fixed(pealkirjad,'\\(',n=2)[,1]  #võtsin kommentaaride arvu ära
    pealkirjad <- str_trim(pealkirjad)
    start_point <- pikkus+1
    end_point <- pikkus+length(pealkirjad)
    pealkirjade_list[start_point:end_point] <- pealkirjad
    rubriik_list[start_point:end_point] <- rubriigid
    kuupaev_list[start_point:end_point] <- kuupaevad
    urls_list[start_point:end_point] <- urls
    pikkus = pikkus+length(pealkirjad)
    url = paste(substr(url,1,url_pre),toString(i+1),sep = "")
  }
  closeAllConnections()
}

closeAllConnections()


sisu_list = rep(NA,200000)
m=1
#m=12
for (u in urls_list[59880:69790]){
  if(m%%5000==0){
    print(m)
    closeAllConnections()
  }
  if(!is.na(u)){
    page <- read_html(u)
    sisu <- page %>% 
      html_nodes("div.article-body__item--htmlElement") %>% 
      html_text()
    sisu <- paste(sisu,collapse = "|")
    sisu_list[m] <- sisu
    m = m + 1
  }else{
    break
  }
}
