library(data.table)
library(dplyr)

dataset_readup <- function(input_path){
  
  dataset <- fread(input_path, stringsAsFactors = FALSE)
  dataset <- as.data.frame(dataset)
  dataset <- dataset[,c("user_id","album_id","artist_id")]
  
  return(dataset)
}

sub_select_image_features <- function(input_path){
  
  dataset <-  fread(input_path, stringsAsFactors = FALSE)
  dataset <- data.frame(dataset)
  dataset <- dataset[, apply(dataset, 2 , mean) > 0]
  
  for(i in 2:ncol(dataset)){
    
    dataset[, i] <- dataset[, i] + 0.01
    dataset[, i] <- log(dataset[, i])
    dataset[, i] <- round(dataset[, i], 5)

  }  
  
  return(dataset)
}

image_dataset_save <- function(dataset, user, album, artist, out_path){

   dataset <- left_join(dataset, user)
   dataset <- left_join(dataset, album)
   dataset <- left_join(dataset, artist)
  
   dataset[is.na(dataset)] <- 0
   print(dataset)
   dataset <- do.call(data.frame,lapply(dataset, function(x) replace(x, is.infinite(x),NA)))
   
   write.csv(dataset[,4:ncol(dataset)], out_path, row.names = FALSE)
}

train <- dataset_readup("./raw_dataset/train_deduplicated.csv")
test <- dataset_readup("./raw_dataset/test.csv")

album <- sub_select_image_features("./raw_dataset/album_images.csv")
user <- sub_select_image_features("./raw_dataset/user_images.csv")
artist <- sub_select_image_features("./raw_dataset/artist_images.csv")

image_dataset_save(train, user, album, artist,  "./clean_dataset/train_aux_image.csv")
image_dataset_save(test, user, album, artist,  "./clean_dataset/test_aux_image.csv")
