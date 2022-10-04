# Come contribuire nella repo (modus operandi)

1. Prenotarsi nella issue: scrivere nei commenti di ogni issue della quale volete occuparvi (o fatemelo semplicemente sapere) e vi assegno il task in questione.

2. Lavorare su un branch separato con un nome significativo (es. se il comando è /help un nome del branch potrebbe essere help-cmd)

3. A stato abbastanza maturo della funzionalità, aprire una PR sul branch main. Se avete bisogno di cambiare qualcosa, basta segnarla come draft.

4. Il lavoro consiste principalmente nel creare nuovi comandi. È sufficiente basarsi sui comandi già esistenti. Le funzioni, una volta ricevuto il messaggio dall'utente, devono inviare un messaggio a quello stesso utente prendendo il testo dal JSON a seconda del comando digitato. Ad esempio /help dovrà rispondere all'utente con frasi['cmd_help']. Leggere approfonditamente il sorgente del bot.

Dare un'occhiata anche all'[issue riepilogativo](https://github.com/dag7dev/MozItaReBot/issues/1).
