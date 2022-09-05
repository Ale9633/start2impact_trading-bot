# Start2impact Python exercise: Trading bot
### Exercise to practice the CoinMarketCap API.<br /><br />
Bot checks every 10 minutes if more than 4 currencies have **increased** in price by **more than 3%** in the last hour: in this case, it will open a *buy* order for the currency that recorded the greatest increase.
If the purchased currency **drops** by **more than 1%** in the last hour, Bot will close the order by *selling* the currency.[^1]
<br /><br />
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187061461-3267dbcb-9361-4295-a126-8a5d849ed736.png"/>
</p>



[^1]: *You can open only one Order at a time*
