library("dplyr")

elu24_dict <- read.csv("elu24_dict.csv",encoding="utf-8",header = F)


elu24_dict %>% 
  slice_max(V2,n=10) %>% 
  print()

postimees_dict <- read.csv("postimees_dict.csv",encoding="utf-8",header = F)

postimees_dict %>% 
  slice_max(V2,n=15) %>% 
  print()

paevaleht_dict <- read.csv("paevaleht_dict.csv",encoding="utf-8",header = F)

paevaleht_dict %>% 
  slice_max(V2,n=15) %>% 
  print()


telegram_dict <- read.csv("telegram_dict.csv",encoding="utf-8",header = F)

telegram_dict %>% 
  slice_max(V2,n=15) %>% 
  print()


ohtuleht_dict <- read.csv("ohtuleht_dict.csv",encoding="utf-8",header = F)

ohtuleht_dict %>% 
  slice_max(V2,n=10) %>% 
  print()


err_dict <- read.csv("err_dict.csv",encoding="utf-8",header = F)

err_dict %>% 
  slice_max(V2,n=12) %>% 
  print()
