Readme

This project is the prototype of predicting future price variation of a NSE stock. The functionality of this prototype includes
predictive analysis, sentimental analysis and Kaleyra messaging and voice call service.

Technology Stack:
1. Microsoft Azure
2. Ruby on Rails
3. Python

Brief about the modules:
1. Price Trigger Alert Module:
This module is a user friendly piece of code with a front end web form. The user provides the details including Stock name, triggering cap and floor values etc.
In this user can check for the service which he/she wants to opt for when the alert gets triggered. The services provided are messaging and
the calling service with the updated the CMP (current market price).

2. Predictive High-Low Module:
This module is based on implementation of Recurrent Neural Network and LSTN. Also, the studies of Bollinger bands (which is a key parameter for stock trading).
In this module the user gets the message with the Highs and Lows of the stock at the end of the day. The user can be a large scale trading firm
or a standalone trader. The pros of this module is that the user is updated with the predictive data of upcoming 7 trading sessions.

3. News Sentimental analysis Module:
Module is based on sentimental analysis model. Where a user will be updated with the sentiments of the latest news related to the subscribed stock.
In this module the news can be scrapped by multiple sources like MoneyControl
