library(data.table)
library(dplyr)

#--------------------------------------------------------------------------
# We drop user-song pairs that appear for the 2nd time.
# We also aggregate the target variable -- mean on the given son per user.
#--------------------------------------------------------------------------

test <- fread("./raw_dataset/test.csv", stringsAsFactors = FALSE)
test <- data.frame(test)

train <- fread("./raw_dataset/train.csv", stringsAsFactors = FALSE)
train <- data.frame(train)

fun <- aggregate(train$is_listened, by = list(train$media_id, train$user_id), mean)

colnames(fun) <- c("media_id", "user_id", "is_listened")

train <- train[!duplicated(train[,c("user_id", "media_id")]), colnames(train) != "is_listened"]
train <- left_join(train, fun)
write.csv(train, "./raw_dataset/train_deduplicated.csv", row.names = FALSE)
