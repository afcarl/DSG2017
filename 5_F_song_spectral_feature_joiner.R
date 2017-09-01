library(data.table)
library(dplyr)

test <- fread("./raw_dataset/test.csv", stringsAsFactors = FALSE)
test <- data.frame(test)

train <- fread("./raw_dataset/train_deduplicated.csv", stringsAsFactors = FALSE)
train <- data.frame(train)

mel_features <- fread("./clean_dataset/clean_mel_features.csv", stringsAsFactors = FALSE, check.names = FALSE)
mel_features <- data.frame(mel_features)

test <- left_join(test, mel_features)
test[is.na(test)] <- 0
print(colnames(test))

test <- test[,paste0("mel_features_",c(1:40))]
write.csv(test,"./clean_dataset/mel_features_test.csv",  row.names = FALSE)
print(colnames(test))


train <- left_join(train, mel_features)
train <- train[,paste0("mel_features_",c(1:40))]

for (i in 1:40){
  print(i)
  train[is.na(train[,i]),i] <- 0
}


write.csv(train,"./clean_dataset/mel_features_train.csv", row.names = FALSE)
print(colnames(train))
