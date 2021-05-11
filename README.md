# bug-facebook-profoundly

## Facebook Profoundly bug 2019/3/9.
This bug allows you to view other people's messages, even an anonymous message through Profoundly, an anonymous ask & answer Facebook app.  
Source (Vietnamese): https://vietthao2000.com/profoundly-co-that-su-an-danh/ -> unfortunately removed :(

Basically there was an endpoint which Profoundly used to get messages of players every time they use the app, without any authentication.
```
https://web.neargroup.me/ng/GetAllMessages?playerId=<player-id>
```

The return JSON data includes sender id, receiver id, firstname of sender and more importantly the content of the message.

## Update 2019/3/12: 
This bug is fixed by moving to another server and change the format of the JSON response. We can no longer see the sender but still can see all the messages ;)

## Update:
This bug is completely fixed by moving to another server and use an authentication token.  
2019/4/18: I found the game deleted on Facebook :D
