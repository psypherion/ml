df <- read.csv("F:/ai_ml/ml_dl_py_r/Data_Files/House_Price.csv", header = TRUE)
str(df)
summary(df)
hist(df$crime_rate)
pairs(~price+crime_rate+n_hot_rooms+rainfall, data = df)
barplot(table(df$airport))
barplot(table(df$waterbody))
barplot(table(df$bus_ter))

# n_hot_rooms and rainfall has outliers
# bus_term is useless
# crime rate has some different relation with price

# CAPPING AND FLOORING:
quantile(df$n_hot_rooms, 0.99)
up = 3*quantile(df$n_hot_rooms, 0.99)
df$n_hot_rooms[df$n_hot_rooms > up ] <- up
summary(df$n_hot_rooms)
lp = 0.3*quantile(df$rainfall, 0.01)
df$rainfall[df$rainfall < lp ] <- lp
summary(df$rainfall)

mean(df$n_hos_beds)
mean(df$n_hos_beds, na.rm = TRUE)
which(is.na(df$n_hos_beds))
df$n_hos_beds[is.na(df$n_hos_beds)] <- mean(df$n_hos_beds, na.rm = TRUE)
summary(df$n_hos_beds)
which(is.na(df$n_hos_beds))

pairs(~price+crime_rate,data=df)
plot(df$price,df$crime_rate)
df$crime_rate = log(1+df$crime_rate)
plot(df$price,df$crime_rate)

df$avg_dist = (df$dist1+df$dist2+df$dist3+df$dist4)/4
df2 <- df[,-7:-10]
df <- df2
df3 <- df[,-14]
df <- df3

install.packages("dummies")
df <- dummy.data.frame(df, sep = ".")

df <- df[,-9]
df <- df[,-14]

cor(df)
round(cor(df),2)

df <- df[,-16]
