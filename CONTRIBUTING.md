# Linee guida per contribuire

## Come contribuire

- **Come fare un commit in maniera efficiente**: https://www.conventionalcommits.org/en/v1.0.0/#summary

1. (opzionale) Aprire un issue relativa al cambiamento che state facendo

2. Lavorare **su un branch separato** con un nome significativo (es. se il comando è `/help` un nome del branch potrebbe essere `help-cmd`)

3. A stato maturo della funzionalità, aprire una PR sul branch main. Se avete bisogno di cambiare qualcosa, basta segnarla come `draft`.

## Env file
Non appesantire l'env file, aggiungendo variabili e stringhe inutili.

## Gestire il numero di versione
- x.y.z dove x è major, y minor e z è patch:
    - x non dovrebbe venire incrementato, a meno che non venga cambiata la libreria o si modificano le funzioni in modo non retrocompatibile
        - ad esempio siamo alla versione 1.0.0: il comando info produce la lista dei colori preferiti del tuo compagno di merende --> x viene incrementato di 1 --> 2.0.0
    - y viene incrementato solo se vengono aggiunte nuove funzionalità
        - ad esempio siamo alla versione 1.0.0: viene aggiunta una funzionalità per fare il caffé --> y viene incrementato di 1 --> 1.1.0
    - z viene incrementato solo se vengono fatti cambiamenti considerati minimi (es. bugfix)
        - ad esempio siamo alla versione 1.0.0: viene corretto un bug --> z viene incrementato di 1 --> 1.0.1
