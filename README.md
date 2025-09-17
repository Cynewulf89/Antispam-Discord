
🤖 Bot Anti-Spam Discord – "Silence"

Bot Discord conçu pour muter automatiquement les spammeurs et supprimer leurs messages.  
Facile à configurer, fonctionne en quelques minutes.

---

📚 Sommaire

1. ⚙️ Préparation du bot Discord
2. 📥 Télécharger et configurer le projet
3. 🚀 Fonctionnement du bot
4. 🐳 Utilisation avec Docker (optionnel)

---

⚙️ Préparation du bot Discord

1. Créer un bot et l’ajouter à votre serveur

    - Va ici : https://discord.com/developers/applications
    - Clique sur "New Application"
    - Donne un nom à ton bot (ex : BotAntiSpam), puis clique sur "Create"

2. Créer le bot dans l'application

    - Dans le menu de gauche, clique sur "Bot"
    - Clique sur "Add Bot", puis "Yes, do it!"
    - (Optionnel) Personnalise le nom ou l'avatar de ton bot

3. Copier le token

    - Toujours dans l'onglet "Bot", clique sur "Reset Token" si besoin
    - Copie le token et colle-le dans ton fichier `.env` comme ceci :
        TOKEN=ton_token_ici

4. Activer les intents

    Active les intents suivants :
    - MESSAGE CONTENT INTENT ✅
    - SERVER MEMBERS INTENT ✅

5. Inviter le bot sur ton serveur

    - Va dans OAuth2 > URL Generator
    - Scopes : coche "bot"
    - Permissions : coche
        - Send Messages
        - Manage Roles
        - Read Message History
        - View Channels
        - Manage Messages
    - Copie l’URL générée et ouvre-la pour inviter le bot

---

📥 Télécharger et configurer le projet

1. Cloner le projet

    git clone https://gitlab.com/Cynewulf89/bot-antispam-discord.git
    cd bot-antispam-discord

2. Installer les dépendances

    pip install -r requirements.txt

3. Créer un fichier `.env`

    TOKEN=ton_token_de_bot
    LOG_CHANNEL_ID=id_du_canal_logs
    MENTION_ID=id_du_role_mentionné

    - LOG_CHANNEL_ID : clic droit sur un salon → "Copier l’identifiant"
    - MENTION_ID : clic droit sur un rôle → "Copier l’identifiant"

---

🚀 Fonctionnement du bot

Lorsque 3 messages identiques sont envoyés en moins d'une minute :

- L'utilisateur est mute automatiquement (rôle "Silence")
- Tous ses rôles sont retirés
- Ses messages sont supprimés (5 dernières minutes)
- Un message de log est posté dans le canal défini avec un ping du rôle mentionné
- Le message contient aussi la commande pour le unmute : !Silence @utilisateur

---

🐳 Utilisation avec Docker (optionnel)

1. Construire l’image Docker :
    sudo docker build -t silence .

2. Lancer le conteneur en arrière-plan :
    sudo docker run -d --name silence silence

---


