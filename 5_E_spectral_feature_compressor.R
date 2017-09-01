library(data.table)

features <- fread("./clean_dataset/mel_features.csv", check.names = FALSE)

features <- data.frame(features)

id <- features$media_id

features <- features[,2:ncol(features)]

pc <- prcomp(features)

pc <- data.frame(pc$x[,1:40])

pc$media_id <- id

colnames(pc) <- c(paste0("mel_features_", c(1:40)), "media_id")

for(i in 1:40){
  
  pc[,i] <- round(pc[,i],5)
  print(i)
  
}

write.csv(pc, "./clean_dataset/clean_mel_features.csv", row.names = FALSE)
