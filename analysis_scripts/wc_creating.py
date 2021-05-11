from wordcloud import WordCloud

portal = "telegram"

with open ("no_stop_" + portal + ".txt", "r", encoding="utf-8") as myfile:
    data=myfile.readline()
    
wordcloud = WordCloud().generate(data)
wordcloud.to_file(portal + '_wc.png')