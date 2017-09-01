library(lubridate)
library(anytime)
library(data.table)
library(dplyr)

dataset_readup_transform <- function(path){
  
  dataset <- fread(paste0("./raw_dataset/", path), stringsAsFactors = FALSE)
  dataset <- data.frame(dataset)
  
  return(dataset)
}

create_id_list <- function(train, test){
  
  id <- c("media_id", "album_id", "user_id", "artist_id","genre_id")
  
  id_list <-  list()
  
  for (i in 1:5){
    
    id_list[[id[i]]] <- c(id_list[id[i]], intersect(unique(train[,id[i]]), unique(test[,id[i]])))
  }
  return(id_list)
}

dummygen <- function(new_table, original_table, dummified_column, column_values, new_name){ 
  
  #------------------------------------------------------------------------------
  # INPUT 1. -- The new cleaned table -- I will attach the dummies to this table.
  # INPUT 2. -- The original table that is being cleaned.
  # INPUT 3. -- The column that has the strings.
  # INPUT 4. -- The unique values in the column encoded.
  # INPUT 5. -- The new name of the columns.
  # OUTPUT -- The new table with the dummy variables.
  #------------------------------------------------------------------------------
  
  i <- 0
  
  for (val in column_values){
    i <- i + 1
    new_variable <- data.frame(matrix(0, nrow(new_table), 1))
    new_variable[original_table[,dummified_column] == val, 1] <- 1
    colnames(new_variable) <- paste0(new_name, i)
    new_table <- cbind(new_table,new_variable)
  }
  
  return(new_table)
}

data_cleaner <- function(input_dataset, media_ids, album_ids, user_ids, artist_ids, genre_ids, is_train){
  
  output_dataset <- data.frame(input_dataset$media_id, input_dataset$genre_id)
  
  colnames(output_dataset) <-c("media_id", "genre_id")
  
  output_dataset$media_id <- replace(output_dataset$media_id,!(output_dataset$media_id %in% media_ids),-1)
  output_dataset$genre_id <- replace(output_dataset$genre_id,!(output_dataset$genre_id %in% genre_ids),-1)
  
  output_dataset$album_id <- input_dataset$album_id
  
  output_dataset$album_id <- replace(output_dataset$album_id,!(output_dataset$album_id %in% album_ids),-1)
  
  output_dataset$user_id <- input_dataset$user_id
  
  output_dataset$user_id <- replace(output_dataset$user_id,!(output_dataset$user_id %in% user_ids),-1)
  
  output_dataset <- dummygen(output_dataset, input_dataset, "context_type", c(1,5,20,25), "context_type_")
  
  date_var <- paste0(substr(as.character(input_dataset$release_date),1,4),"-",substr(as.character(input_dataset$release_date),5,6),"-",substr(as.character(input_dataset$release_date),7,8))
  
  output_dataset$year <- lubridate::year(date_var)
  
  output_dataset$month <-  lubridate::month(date_var)
  
  output_dataset$day <- lubridate::day(date_var)
  
  new_date_var <- anydate(input_dataset$ts_listen)
  
  output_dataset$month_2 <-  lubridate::month(new_date_var)
  
  output_dataset$day_2 <- lubridate::day(new_date_var)
  
  output_dataset$hours <- lubridate::hour(anytime(input_dataset$ts_listen))
  
  output_dataset$wday <- lubridate::wday(anytime(input_dataset$ts_listen))
  
  output_dataset <- dummygen(output_dataset, input_dataset, "platform_name", c(0, 1, 2), "platform_name_")
  
  output_dataset <- dummygen(output_dataset, input_dataset, "platform_family", c(0, 1, 2), "platform_family_")  
  
  output_dataset$context_type<- input_dataset$context_type
  
  output_dataset$media_duration <- input_dataset$media_duration
  
  output_dataset$listen_type <- input_dataset$listen_type
  
  output_dataset$user_gender <- input_dataset$user_gender  
  
  output_dataset$artist_id <-input_dataset$artist_id 
  
  output_dataset$artist_id <- replace(output_dataset$artist_id,!(output_dataset$artist_id %in% artist_ids),-1)
  
  output_dataset$user_age <- input_dataset$user_age
  
  return(output_dataset)
  
}



join_up_aggregates <- function(dataset, aggregates){
  
  for (aggregate in aggregates){
    
    aggregate_table <- read.csv(paste0("./raw_dataset/", aggregate), sep = ",", stringsAsFactors = FALSE)
    dataset <- left_join(dataset, aggregate_table)
    
  }
  return(dataset)
}


drop_columns <- function(dataset, where_to_drop){
  
  #---------------------------------------
  #
  #
  #
  #
  #---------------------------------------
  
  dataset <- dataset[, setdiff(colnames(dataset), c("user_id","artist_id","media_id","genre_id","album_id","context_type"))]
  dataset[is.na(dataset)] <- -1
  
  print(colnames(dataset))
  
  write.csv(dataset, where_to_drop, row.names = FALSE)
  
  return(dataset)
}


test <- dataset_readup_transform("test.csv")
train <- dataset_readup_transform("train_deduplicated.csv")

target <- data.frame(train$is_listened)
write.csv(target, "./clean_dataset/target.csv", row.names = FALSE)


id_list <- create_id_list(train, test)

clean_test <- data_cleaner(test,
                           unlist(id_list["media_id"]),
                           unlist(id_list["album_id"]),
                           unlist(id_list["user_id"]),
                           unlist(id_list["artist_id"]),
                           unlist(id_list["genre_id"]),
                           FALSE)

clean_train <- data_cleaner(train,
                            unlist(id_list["media_id"]),
                            unlist(id_list["album_id"]),
                            unlist(id_list["user_id"]),
                            unlist(id_list["artist_id"]),
                            unlist(id_list["genre_id"]),
                            TRUE)

aggregates <- c("user_aggregates.csv",
                "media_aggregates.csv",
                "media_user_aggregates.csv",
                "artist_aggregates.csv",
                "album_aggregates.csv",
                "genre_aggregates.csv",
                "user_special_aggregates.csv",
                "album_special_aggregates.csv",
                "media_special_aggregates.csv",
                "artist_special_aggregates.csv",
                "genre_special_aggregates.csv",
                "user_special_aggregates_2.csv",
                "album_special_aggregates_2.csv",
                "media_special_aggregates_2.csv",
                "artist_special_aggregates_2.csv",
                "genre_special_aggregates_2.csv")


clean_train <- join_up_aggregates(clean_train, aggregates)
clean_test <- join_up_aggregates(clean_test, aggregates)

clean_test <- drop_columns(clean_test[5:ncol(clean_test)], "./clean_dataset/test.csv")
clean_train <- drop_columns(clean_train[5:ncol(clean_train)], "./clean_dataset/train.csv")
