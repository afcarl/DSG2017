library(data.table)
library(dplyr)

test <- fread("./raw_dataset/test.csv", stringsAsFactors = FALSE)
test <- data.frame(test)

train <- fread("./raw_dataset/train.csv", stringsAsFactors = FALSE)
train <- data.frame(train)

train <- train[train$context_type == 1 | train$context_type == 5| train$context_type == 20| train$context_type == 25 ,]

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

user_means <- aggregate(train$is_listened,  by = list(train$user_id),mean)
user_sums <- aggregate(rep(1,nrow(train)),  by = list(train$user_id),sum)

colnames(user_means) <- c("user_id","user_is_listened_2")
colnames(user_sums) <- c("user_id","user_counts_2")

user <- left_join(user_means, user_sums)
user <- user[(user$user_counts_2 > 10),]

write.csv(user,"./raw_dataset/user_special_aggregates.csv",row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

media_means <- aggregate(train$is_listened ,  by = list(train$media_id),mean)
media_sums <- aggregate(rep(1,nrow(train)),  by = list(train$media_id),sum)

colnames(media_means) <- c("media_id","media_is_listened_2")
colnames(media_sums) <- c("media_id","media_counts_2")

media <- left_join(media_means, media_sums)
media <- media[(media$media_counts_2 > 10),]

write.csv(media ,"./raw_dataset/media_special_aggregates.csv",row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

genre_means <- aggregate(train$is_listened,  by = list(train$genre_id),mean)
genre_sums <- aggregate(rep(1,nrow(train)),  by = list(train$genre_id),sum)

colnames(genre_means) <- c("genre_id","genre_is_listened_2")
colnames(genre_sums) <- c("genre_id","genre_counts_2")

genre <- left_join(genre_means, genre_sums)
genre <- genre[(genre$genre_counts_2 > 10),]

write.csv(genre,"./raw_dataset/genre_special_aggregates.csv",row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

album_means <- aggregate(train$is_listened,  by = list(train$album_id),mean)
album_sums <- aggregate(rep(1,nrow(train)),  by = list(train$album_id),sum)

colnames(album_means) <- c("album_id","album_is_listened_2")
colnames(album_sums) <- c("album_id","album_counts_2")

album <- left_join(album_means, album_sums)
album <- album[(album$album_counts_2 > 10),]

write.csv(album,"./raw_dataset/album_special_aggregates.csv",row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

artist_means <- aggregate(train$is_listened,  by = list(train$artist_id),mean)
artist_sums <- aggregate(rep(1,nrow(train)),  by = list(train$artist_id),sum)

colnames(artist_means) <- c("artist_id","artist_is_listened_2")
colnames(artist_sums) <- c("artist_id","artist_counts_2")

artist <- left_join(artist_means, artist_sums)
artist <- artist[(artist$artist_counts_2 > 10),]

write.csv(artist, "./raw_dataset/artist_special_aggregates.csv", row.names = FALSE)
