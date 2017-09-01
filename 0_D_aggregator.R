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

user_means <- aggregate(train$is_listened,  by = list(train$user_id, train$context_type), mean)
user_sums <- aggregate(rep(1, nrow(train)),  by = list(train$user_id, train$context_type), sum)

colnames(user_means) <- c("user_id", "context_type", "user_is_listened_3")
colnames(user_sums) <- c("user_id", "context_type", "user_counts_3")

user <- left_join(user_means, user_sums)
user <- user[(user$user_counts_3 > 10),]

write.csv(user, "./raw_dataset/user_special_aggregates_2.csv", row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

media_means <- aggregate(train$is_listened,  by = list(train$media_id, train$context_type), mean)
media_sums <- aggregate(rep(1, nrow(train)),  by = list(train$media_id, train$context_type), sum)

colnames(media_means) <- c("media_id", "context_type", "media_is_listened_3")
colnames(media_sums) <- c("media_id", "context_type", "media_counts_3")

media <- left_join(media_means, media_sums)
media <- media[(media$media_counts > 10),]

write.csv(media ,"./raw_dataset/media_special_aggregates_2.csv", row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

genre_means <- aggregate(train$is_listened,  by = list(train$genre_id,  train$context_type), mean)
genre_sums <- aggregate(rep(1, nrow(train)),  by = list(train$genre_id,  train$context_type), sum)

colnames(genre_means) <- c("genre_id", "context_type", "genre_is_listened_3")
colnames(genre_sums) <- c("genre_id", "context_type", "genre_counts_3")

genre <- left_join(genre_means, genre_sums)
genre <- genre[(genre$genre_counts > 10),]

write.csv(genre,"./raw_dataset/genre_special_aggregates_2.csv", row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

album_means <- aggregate(train$is_listened,  by = list(train$album_id,  train$context_type), mean)
album_sums <- aggregate(rep(1, nrow(train)),  by = list(train$album_id,  train$context_type), sum)

colnames(album_means) <- c("album_id", "context_type", "album_is_listened_3")
colnames(album_sums) <- c("album_id", "context_type", "album_counts_3")

album <- left_join(album_means, album_sums)
album <- album[(album$album_counts_3 > 10),]

write.csv(album,"./raw_dataset/album_special_aggregates_2.csv", row.names = FALSE)

#----------------------------------------------------------------
#
#
#
#----------------------------------------------------------------

artist_means <- aggregate(train$is_listened,  by = list(train$artist_id,  train$context_type), mean)
artist_sums <- aggregate(rep(1, nrow(train)),  by = list(train$artist_id,  train$context_type), sum)

colnames(artist_means) <- c("artist_id", "context_type", "artist_is_listened_3")
colnames(artist_sums) <- c("artist_id", "context_type", "artist_counts_3")

artist <- left_join(artist_means, artist_sums)
artist <- artist[(artist$artist_counts_3 > 10),]

write.csv(artist, "./raw_dataset/artist_special_aggregates_2.csv", row.names = FALSE)
