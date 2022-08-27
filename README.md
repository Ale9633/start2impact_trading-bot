# Start2impact Python exercise: Trading bot
### Esercizio per fare pratica con le API di CoinMarketCap.<br /><br />
Il Bot controlla ogni 10 minuti se più di 4 valute sono aumentate di prezzo di **oltre il 3% nell'ultima ora**: in questo caso, aprirà un ordine di acquisto per la valuta che ha registrato l'incremento maggiore.
Se la valuta acquistata scende di **oltre l'1% nell'ultima ora**, il Bot chiuderà l'ordine vendendo la valuta.<br /><br />
<sup>*(È possibile aprire un solo ordine alla volta)*</sup>
