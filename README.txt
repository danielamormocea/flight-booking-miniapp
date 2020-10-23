Tema2 - SPRC -
Mormocea Daniela 342C5

Am implementat toate functionalitatile descrise in cerinta, folosing Python
si Flask. Astfel, am modulul app-admin ce reprezinta aplicatia de administrare,
unde este prezent fisierul app-admin.py. Acesta contine baza de date si cele 2
tabele de care m-am folosit in restul temei: o tabela flights ce contine toate
informatiile pentru un zbor, precum si un camp cu numarul de rezervari posibile
si o table reservations pentru a mentine legatura id-reservare <-> id zbor.
Administratorul poate comunica cu baza de date prin interfata text.

Mai am fisierul client.py din serviciul client care citeste de la tastatura
cerintele clientului si le trimite la server.

In final am si server.py, un serviciu scris in flask care primeste jsoanele
de la client si unde calculez in prima faza ruta optima, cu bfs, pornind de la
un hashtable ce contine toate sursele si detaliile de zbor asociate, in final
intorcandu-i clientului un dictionar cu toate zborurile calculate in functie de
preferintele lui. In metoda bookTicket verific in baza de date daca se poate face
rezervarea biletelor cerute de client, returnand un reservation ID, ca mai apoi
in buyTicket, clientul sa poata folosi acel reservation ID si sa cumpere toate
zborurile asociate calatoriei lui. In final, aceasta metoda intoarce o lista
cu toate zborurile si detaliile acestora. 


!!!!DETALII LEGATE DE RULAREA TEMEI!!!!:

Pentru a lega toate dockerele am folosit docker compose. Se da build (docker 
compose up --build) intr-un terminal in folderul root, in alt terminal pentru a
deschide clientul folosim comanda: docker attach tema2_client_1 si apoi se apasa
enter, iar pentru aplicatia de administrare, in cazul in care se doreste o 
comunicare cu baza de date, putem in alt terminal sa deschidem iar cu attach:
docker attach tema2_app-admin_1 si tot este nevie de un enter apoi. 



Mentionez ca tema mai poate avea niste scapari, intrucat nu cred ca am putut
testa si acoperi chiar toate cazurile. In mare, ar trebui sa mearga.


