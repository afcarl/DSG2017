library(data.table)
library(dplyr)

train <- fread("./raw_dataset/train_deduplicated.csv",stringsAsFactors = FALSE)
target <- read.csv("./clean_dataset/target.csv",stringsAsFactors = FALSE)

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

train <- as.data.frame(train)
train <- train[,c("user_id","media_id","album_id","artist_id")]
test <- read.csv("./raw_dataset/test.csv",stringsAsFactors = FALSE)
test <- test[,c("user_id","media_id","album_id","artist_id")]

test_likes <- read.csv("./raw_dataset/test_likes.csv",stringsAsFactors = FALSE)
train_likes <- read.csv("./raw_dataset/train_likes.csv",stringsAsFactors = FALSE)

test_language <- read.csv("./raw_dataset/language_test.csv",stringsAsFactors = FALSE)
train_language <- fread("./raw_dataset/language_train.csv",stringsAsFactors = FALSE)

train_language <- data.frame(train_language)

media <-  fread("./raw_dataset/media_augmented_data.csv",stringsAsFactors = FALSE)
media <- data.frame(media)

user <- read.csv("./raw_dataset/user_augmented_data.csv",stringsAsFactors = FALSE)
artist <- read.csv("./raw_dataset/artist_augmented_data.csv",stringsAsFactors = FALSE)
album <- read.csv("./raw_dataset/album_augmented_data.csv",stringsAsFactors = FALSE)

#------------------------------------

user[is.na(user)] <- ""

#------------------------------------

clean_media <- data.frame(media$media_id)

colnames(clean_media) <- c("media_id")

clean_media$track_available_countries <- media$track_available_countries

clean_media$track_disk_number <- media$track_disk_number

clean_media$track_explicit <- 0

clean_media$track_explicit[media$track_explicit == TRUE]  <- 1

clean_media$track_gain <- media$track_gain

clean_media$track_rank <- media$track_rank

clean_media$track_contri <- media$track_contri

clean_media$track_posi <- media$track_posi

clean_media$track_bpm <- media$track_bpm

#------------------------------------

test <- left_join(test,clean_media)
train <- left_join(train,clean_media)

#------------------------------------

clean_artist <- data.frame(artist$artist_id)

colnames(clean_artist) <- c("artist_id")

clean_artist$radio_1 <- 0

clean_artist$radio_1[artist$artist_radio== "True"] <- 1

clean_artist$radio_2 <- 0
clean_artist$radio_2[artist$artist_radio== "False"] <- 1

clean_artist$artist_fans <- artist$artist_fans
clean_artist$artist_albums_num <- artist$artist_albums_num

#------------------------------------

test <- left_join(test, clean_artist)
train <- left_join(train, clean_artist)

#------------------------------------

album_aggs <- aggregate(rep(1,nrow(album)),by = list(album$album_label),sum)

album_aggs_base <- album_aggs
album_aggs <- album_aggs[album_aggs$x,]
colnames(album_aggs_base) <- c("album_label","label_aggregates")
album_extra <- left_join(album,album_aggs_base)
albums <- album_aggs[,1]

clean_album <- data.frame(album$album_id)

colnames(clean_album) <- c("album_id")

clean_album$album_duration <- album$album_duration

clean_album$album_explicit <- 0

clean_album$album_explicit[album$album_explicit == "True"] <- 1

clean_album$album_nb_tracks <- album$album_nb_tracks
clean_album$album_fans <- album$album_fans

clean_album$album_rec_1 <- 0

clean_album$album_rec_1[album$album_record_type == "single"] <- 1

clean_album$album_rec_2 <- 0

clean_album$album_rec_2[album$album_record_type == "ep"] <- 1

clean_album$album_rec_3 <- 0

clean_album$album_rec_3[album$album_record_type == "compile"] <- 1

clean_album$album_rec_4 <- 0

clean_album$label_aggregates <- album_extra$label_aggregates

clean_album$album_rec_4[album$album_record_type == "album"] <- 1

#---------------------------------------------

test <- left_join(test,clean_album)
train <- left_join(train,clean_album)

#----------------------------------------

sums <- aggregate(rep(1, length(train_language$song_country)), by = list(train$media_id, train_language$song_registrant), sum)
sums <- aggregate(rep(1, nrow(sums)), by = list(sums$Group.2), sum)
sums <- sums[sums$x>200,]

useful_languages <- intersect(unique(test_language$song_country), train_language$song_country)

useful_registrants <- intersect(unique(test_language$song_registrant),sums$Group.1)

clean_test_language <- test_language[,c("registry_year","id_number","same_country_reg","song_not_allowed")]
clean_train_language <- train_language[,c("registry_year","id_number","same_country_reg","song_not_allowed")]

clean_test_language$media_readable <- 0 
clean_test_language$media_readable[test_language$media_readable == "False"] <- 1
clean_test_language$media_readable[test_language$media_readable == "0"] <- 1

clean_train_language$media_readable <- 0 
clean_train_language$media_readable[train_language$media_readable == "False"] <- 1
clean_train_language$media_readable[train_language$media_readable == "0"] <- 1

clean_test_language <- dummygen(clean_test_language , test_language, "song_country", useful_languages, "song_country_")
clean_train_language <- dummygen(clean_train_language, train_language, "song_country", useful_languages, "song_country_")

clean_test_language <- dummygen(clean_test_language , test_language, "song_registrant", useful_registrants, "registrant_")
clean_train_language <- dummygen(clean_train_language, train_language, "song_registrant", useful_registrants, "registrant_")


#---------------------------------------------

train <- cbind(train, clean_train_language)
test <- cbind(test, clean_test_language)

#---------------------------------------------

nations <- unique(user$nationality)
nations <- sort(nations)[2:length(nations)]

clean_user <- data.frame(user$user_id)

colnames(clean_user) <- c("user_id")

clean_user <- dummygen(clean_user, user, "nationality", nations, "nationality_")

#---------------------------------------------

test <- left_join(test, clean_user)
train <- left_join(train, clean_user)

#---------------------------------------------

train <- cbind(train, train_likes)
test <- cbind(test, test_likes)

for (i in 1:ncol(test)){
  print(i)
  test[is.na(test[,i]),i] <- -1
  train[is.na(train[,i]),i] <- -1
}

#---------------------------------------------

write.csv(test[,5:ncol(test)], "./clean_dataset/test_aux.csv", row.names = FALSE)
write.csv(train[,5:ncol(train)], "./clean_dataset/train_aux.csv", row.names = FALSE)
