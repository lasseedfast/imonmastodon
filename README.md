A Twitter bot to collect Mastodon usernames from Twitter users. By mentioning [@imonmastodon](https://twitter.com/imonmastodon) and then writing a Mastodon username the twitter user connects her or his Twitter name with the one on Mastodon. Eg:  
```@imonmastodon! My nick is @lasseedfast@mas.to```  
 The usernames are put in a PostgreSQL database available to other services trying to connect new Mastodon users with their old Twitter friends. Please let me know if you're running such a service and find the idea of an open and collaborative database interesting! Me on [Twitter](https://twitter.com/lasseedfast) and [Mastodon](https://mas.to/@lasseedfast).

Connect to the database (read only) with:  
```postgres://everyone:imonmastodon@imonmastodon.cx58bph3yf7h.us-east-1.rds.amazonaws.com:5432/imonmastodon```

I've just started this project and will fill out this readme more soon.
