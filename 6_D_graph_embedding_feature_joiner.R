library(data.table)
library(dplyr)

dataset_readup <- function(input_path){
  
  dataset <- fread(input_path, stringsAsFactors = FALSE)
  dataset <- as.data.frame(dataset)
  dataset <- dataset[,c("user_id","media_id")]
  
  return(dataset)
}

train <- dataset_readup("./raw_dataset/train_deduplicated.csv")
test <- dataset_readup("./raw_dataset/test.csv")

graph_embeddings <- fread("./raw_dataset/node_2_vec.csv")

graph_embeddings <- data.frame(graph_embeddings)

colnames(graph_embeddings)[1] <- "user_id"

train <- left_join(train, graph_embeddings)
test <- left_join(test, graph_embeddings)  


colnames(graph_embeddings)[1] <- "media_id"
colnames(graph_embeddings)[2:65] <- paste0("media_embed_",c(0:63))

train <- left_join(train, graph_embeddings)
test <- left_join(test, graph_embeddings) 

test[is.na(test)] <- 0
train[is.na(train)] <- 0

write.csv(test[,3:130], "./clean_dataset/test_graph.csv",row.names = FALSE)
write.csv(train[,3:130], "./clean_dataset/train_graph.csv",row.names = FALSE)
