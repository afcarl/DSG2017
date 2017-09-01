library(dplyr)
library(data.table)
library(xgboost)

docs <- list.files("./predictions/test/")
docs <- setdiff(docs,c("linear.csv") )

target <- read.csv("./clean_dataset/target.csv")[,1]

data_integrate <- function(main_path, docs){

    for (i in 1:length(docs)){
    if(i==1){
      dataset <- fread(paste0(main_path,docs[i]))
      dataset <- data.frame(dataset)
      dataset[,2] <- round(dataset[,2],5)
    }
    else{
      other_dataset <- fread(paste0(main_path,docs[i]))
      other_dataset <- data.frame(other_dataset)
      other_dataset[,2] <- round(other_dataset[,2],5)
      dataset <- left_join(dataset, other_dataset)
    }
    
  }
  return(dataset[,2:ncol(dataset)])
}


test <- data_integrate("./predictions/test/", docs)
train <- data_integrate("./predictions/train/", docs)

booster <- xgboost(data = as.matrix(train),
                   label = target,
                   eta = 0.1,
                   eval_metric = "auc", 
                   subsample = 1,
                   lambda = 1,
                   alpha = 1,
                   colsample_bytree = 1,
                   booster = "gblinear",
                   nrounds = 100, 
                   objective = "binary:logistic",
                   maximize = TRUE)

yhat <- predict(booster,as.matrix(test))

out <- data.frame(c(0:19917))

colnames(out)[1] <- "sample_id" 
out$is_listened <- yhat

linear <- read.csv("./predictions/test/linear.csv")

out$is_listened <- 0.54*out$is_listened + 0.46*linear$is_listened

write.csv(out,"fun.csv",row.names = FALSE )
