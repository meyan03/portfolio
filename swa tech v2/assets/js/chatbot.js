/* ========================================
   SWA Tech — Chatbot d'assistance
   Assistant guidé (arbre de questions) pour aider
   le visiteur à comprendre SWA Tech, choisir une offre
   et passer à l'action (devis, RDV, contact).
   ======================================== */

(function () {
  "use strict";

  const CONTACT = {
    whatsapp: "https://wa.me/33688782628",
    email: "contact@swa-tech.fr",
    calendar: "https://calendar.app.google/i8C4sXfoNNpZpebq9",
    devisSite: "formulaire.html",
    devisCyber: "formulaire_cyber.html",
  };

  // Chaque noeud : message du bot (HTML simple autorisé) + liste de choix.
  // Un choix peut avoir : next (id du noeud suivant), href (lien externe/interne), ou les deux.
  const TREE = {
    root: {
      message:
        "👋 Bonjour ! Je suis l'assistant de <strong>SWA Tech</strong>. SWA Tech peut vous aider à :",
      choices: [
        { label: "🧭 Comprendre SWA Tech", next: "comprendre" },
        { label: "✨ Ce qui fait la différence", next: "difference" },
        { label: "🛠️ Les activités de SWA Tech", next: "activites" },
        { label: "💻 Choisir mon site web", next: "choix_intro" },
        { label: "💶 Avoir une fourchette de prix", next: "devis_intro" },
        { label: "📅 Prendre rendez-vous", next: "rdv" },
        { label: "📞 Coordonnées / contact", next: "contact" },
      ],
    },

    comprendre: {
      message:
        "<strong>SWA Tech</strong>, c'est l'agence de <strong>Meyan Traoré</strong>, Master Cybersécurité.<br><br>" +
        "L'idée : aider les indépendants, commerçants, TPE/PME et associations à avoir un <strong>site web professionnel ET sécurisé</strong>, sans les tarifs d'agence et sans les sites \"jolis mais troués\" des freelances low-cost.<br><br>" +
        "Vous êtes accompagné·e de A à Z : conception, création du site, sécurisation, mise en ligne et formation pour gérer votre site en autonomie.",
      choices: [
        { label: "✨ En quoi SWA Tech fait la différence ?", next: "difference" },
        { label: "🛠️ Voir les activités proposées", next: "activites" },
        { label: "👩‍💻 En savoir plus sur Meyan", href: "a_propos.html" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    difference: {
      message:
        "✨ <strong>Ce qui différencie SWA Tech :</strong><br><br>" +
        "🔐 <strong>Sécurité intégrée dès la conception</strong> — HTTPS, protection des formulaires, durcissement, bonnes pratiques OWASP. Pas une option qu'on ajoute après coup.<br><br>" +
        "📱 <strong>Design moderne et responsive</strong>, personnalisé à votre image.<br><br>" +
        "🤝 <strong>Accompagnement humain durable</strong> — formation incluse pour gérer votre site vous-même, support après livraison.<br><br>" +
        "💶 <strong>Tarifs accessibles</strong> pour TPE/PME/associations, paiement en 2 fois, sans devis gonflé.<br><br>" +
        "🎓 <strong>Un seul interlocuteur</strong> qui combine développement web ET expertise cybersécurité (SOC, pentest, audit).",
      choices: [
        { label: "🛠️ Voir les activités de SWA Tech", next: "activites" },
        { label: "💻 Choisir mon site web", next: "choix_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    activites: {
      message:
        "🛠️ <strong>Les activités de SWA Tech :</strong><br><br>" +
        "🌐 <strong>Création de sites web</strong> — vitrine, e-commerce, refonte (packs Essentiel, Standard, Professionnel, E-commerce).<br><br>" +
        "🛡️ <strong>Cybersécurité</strong> — audit de sécurité, durcissement, conseils paiement/admin, rapports mensuels.<br><br>" +
        "🎓 <strong>Formations</strong> — prise en main de votre site, autonomie pour modifier textes/images.<br><br>" +
        "🔧 <strong>Maintenance & suivi</strong> — mises à jour, sauvegardes, monitoring, conseil digital mensuel.<br><br>" +
        "Que voulez-vous explorer ?",
      choices: [
        { label: "🌐 Sites web (offres)", href: "offres.html" },
        { label: "🛡️ Cybersécurité", href: "cybersecurite.html" },
        { label: "🎓 Formations", href: "formation_site.html" },
        { label: "💻 M'aider à choisir mon site", next: "choix_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    /* ---------- Choisir son site ---------- */

    choix_intro: {
      message:
        "💻 Pour vous orienter vers le pack le plus adapté, précisez : <strong>avez-vous déjà un site web ?</strong>",
      choices: [
        { label: "Non, je n'ai pas encore de site", next: "choix_pas_de_site" },
        { label: "Oui, mais je veux le refaire", next: "choix_refonte" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    choix_pas_de_site: {
      message:
        "Pas de problème, c'est très fréquent ! Avez-vous besoin de <strong>vendre des produits en ligne</strong> (boutique) ou juste de <strong>présenter votre activité</strong> ?",
      choices: [
        { label: "Vendre des produits / services en ligne", next: "reco_ecommerce" },
        { label: "Présenter mon activité, mes coordonnées", next: "choix_taille_simple" },
        { label: "⬅️ Retour", next: "choix_intro" },
      ],
    },

    choix_refonte: {
      message:
        "D'accord, on parle d'une <strong>refonte</strong>. Votre site actuel a-t-il besoin de quelques pages simples, ou d'un site plus riche (galerie, blog, boutique) ?",
      choices: [
        { label: "Quelques pages, refonte simple", next: "reco_standard" },
        { label: "Site riche : galerie, blog, formulaires avancés", next: "reco_pro" },
        { label: "C'est une boutique en ligne", next: "reco_ecommerce" },
        { label: "⬅️ Retour", next: "choix_intro" },
      ],
    },

    choix_taille_simple: {
      message:
        "Une dernière précision : voulez-vous une <strong>seule page</strong> qui résume tout (one-page), ou <strong>plusieurs pages</strong> (accueil, services, à propos, contact...) ?",
      choices: [
        { label: "Une seule page suffit (one-page)", next: "reco_essentiel" },
        { label: "Plusieurs pages, avec galerie/portfolio/blog", next: "choix_pro_ou_standard" },
        { label: "3 à 5 pages classiques", next: "reco_standard" },
        { label: "⬅️ Retour", next: "choix_pas_de_site" },
      ],
    },

    choix_pro_ou_standard: {
      message:
        "Avez-vous besoin d'une <strong>galerie de réalisations</strong> ou d'un <strong>blog/actualités</strong> ?",
      choices: [
        { label: "Oui, galerie et/ou blog", next: "reco_pro" },
        { label: "Non, pas besoin pour l'instant", next: "reco_standard" },
        { label: "⬅️ Retour", next: "choix_taille_simple" },
      ],
    },

    reco_essentiel: {
      message:
        "✅ Le <strong>Pack Essentiel</strong> est fait pour vous : un site vitrine one-page, présentation de votre activité, coordonnées et réseaux sociaux, design pro, responsive, sécurité de base (HTTPS, headers).<br><br>" +
        "C'est le point de départ idéal pour une première présence en ligne.",
      choices: [
        { label: "💶 Voir la fourchette de prix", next: "devis_essentiel" },
        { label: "📋 Voir le détail des packs", href: "offres.html" },
        { label: "📅 Prendre RDV pour en discuter", next: "rdv" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    reco_standard: {
      message:
        "✅ Le <strong>Pack Standard</strong> est le plus choisi : site vitrine 3 à 5 pages, design personnalisé, section avis clients, formulaire de contact sécurisé, mise en ligne + hébergement, formation 30 min incluse, sécurité OWASP.<br><br>" +
        "Idéal si vous voulez un site complet qui reflète vraiment votre activité.",
      choices: [
        { label: "💶 Voir la fourchette de prix", next: "devis_standard" },
        { label: "📋 Voir le détail des packs", href: "offres.html" },
        { label: "📅 Prendre RDV pour en discuter", next: "rdv" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    reco_pro: {
      message:
        "✅ Le <strong>Pack Professionnel</strong> correspond à votre besoin : site vitrine 5 à 7 pages, galerie/portfolio, blog ou actualités, formulaire avancé, zone admin selon solution, SEO de base, sécurité renforcée.<br><br>" +
        "Parfait pour une image forte et un site riche en contenu.",
      choices: [
        { label: "💶 Voir la fourchette de prix", next: "devis_pro" },
        { label: "📋 Voir le détail des packs", href: "offres.html" },
        { label: "📅 Prendre RDV pour en discuter", next: "rdv" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    reco_ecommerce: {
      message:
        "✅ Le <strong>Pack E-commerce</strong> est adapté : boutique en ligne complète, pages produits (photos + descriptions), panier et processus de commande, design personnalisé, conseils sécurité paiement/admin, formation à la gestion de la boutique incluse.",
      choices: [
        { label: "💶 Voir la fourchette de prix", next: "devis_ecommerce" },
        { label: "📋 Voir le détail des packs", href: "offres.html" },
        { label: "📅 Prendre RDV pour en discuter", next: "rdv" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    /* ---------- Fourchette de devis ---------- */

    devis_intro: {
      message:
        "💶 SWA Tech peut vous donner une <strong>fourchette indicative</strong> selon le type de site. ⚠️ Le tarif final est établi par Meyan après un <strong>diagnostic personnalisé</strong> de votre projet (consultation gratuite).<br><br>" +
        "Quel type de site vous intéresse ?",
      choices: [
        { label: "Site vitrine 1 page (Essentiel)", next: "devis_essentiel" },
        { label: "Site vitrine 3-5 pages (Standard)", next: "devis_standard" },
        { label: "Site riche 5-7 pages (Professionnel)", next: "devis_pro" },
        { label: "Boutique en ligne (E-commerce)", next: "devis_ecommerce" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    devis_essentiel: {
      message:
        "💶 <strong>Pack Essentiel (one-page)</strong> : généralement la formule <strong>la plus accessible</strong> — c'est le tarif d'entrée le plus bas de SWA Tech.<br><br>" +
        "📌 Le prix exact dépend de votre activité, du contenu à créer et de vos options. Paiement en 2 fois possible (40% / 60%).<br><br>" +
        "Pour un <strong>chiffre précis</strong>, c'est Meyan qui l'établit après un échange rapide sur votre besoin.",
      choices: [
        { label: "📋 Remplir le formulaire de devis", href: CONTACT.devisSite },
        { label: "📅 Réserver une consultation gratuite", href: CONTACT.calendar },
        { label: "💻 Voir un autre pack", next: "devis_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    devis_standard: {
      message:
        "💶 <strong>Pack Standard (3-5 pages)</strong> — le pack le plus choisi : tarif <strong>intermédiaire</strong>, au-dessus du pack Essentiel.<br><br>" +
        "📌 Il inclut le design personnalisé, le formulaire sécurisé, l'hébergement et la formation. Le prix varie selon le nombre de pages et le contenu à rédiger. Paiement en 2 fois possible (40% / 60%).<br><br>" +
        "Le montant exact est donné par Meyan après diagnostic de votre projet.",
      choices: [
        { label: "📋 Remplir le formulaire de devis", href: CONTACT.devisSite },
        { label: "📅 Réserver une consultation gratuite", href: CONTACT.calendar },
        { label: "💻 Voir un autre pack", next: "devis_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    devis_pro: {
      message:
        "💶 <strong>Pack Professionnel (5-7 pages)</strong> : tarif <strong>plus élevé</strong> que le Standard, car il inclut une galerie/portfolio, un blog, un formulaire avancé, une éventuelle zone admin et le SEO de base.<br><br>" +
        "📌 Le prix dépend surtout du nombre de pages, de la galerie et des fonctionnalités demandées. Paiement en 2 fois possible (40% / 60%).<br><br>" +
        "Le chiffrage précis est fait par Meyan après diagnostic.",
      choices: [
        { label: "📋 Remplir le formulaire de devis", href: CONTACT.devisSite },
        { label: "📅 Réserver une consultation gratuite", href: CONTACT.calendar },
        { label: "💻 Voir un autre pack", next: "devis_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    devis_ecommerce: {
      message:
        "💶 <strong>Pack E-commerce</strong> : c'est le pack le plus complet, donc le <strong>plus élevé en investissement</strong> — boutique complète, pages produits, panier, sécurité paiement, formation gestion boutique.<br><br>" +
        "📌 Le prix dépend du nombre de produits, des fonctionnalités (coupons, produits vedettes...) et de la plateforme. Paiement en 2 fois possible (40% / 60%).<br><br>" +
        "Le montant exact est défini par Meyan après un diagnostic de votre activité.",
      choices: [
        { label: "📋 Remplir le formulaire de devis", href: CONTACT.devisSite },
        { label: "📅 Réserver une consultation gratuite", href: CONTACT.calendar },
        { label: "💻 Voir un autre pack", next: "devis_intro" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    /* ---------- RDV / Contact ---------- */

    rdv: {
      message:
        "📅 Le plus simple est de réserver directement une <strong>consultation gratuite de 30 minutes</strong> avec Meyan via Google Calendar — sans engagement.<br><br>" +
        "Vous pouvez aussi passer par WhatsApp pour échanger rapidement avant de prendre rendez-vous.",
      choices: [
        { label: "📅 Réserver mon créneau", href: CONTACT.calendar },
        { label: "💬 Discuter sur WhatsApp", href: CONTACT.whatsapp },
        { label: "📋 Remplir le formulaire de devis site", href: CONTACT.devisSite },
        { label: "🛡️ Remplir le formulaire devis cyber", href: CONTACT.devisCyber },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },

    contact: {
      message:
        "📞 <strong>Coordonnées SWA Tech :</strong><br><br>" +
        "💬 WhatsApp / Appel : <strong>+33 6 88 78 26 28</strong><br>" +
        "☎️ Appel (Mali) : <strong>+223 76 76 67 58</strong><br>" +
        "📧 Email : <strong>contact@swa-tech.fr</strong><br>" +
        "🌐 Site : <strong>www.swa-tech.fr</strong><br>" +
        "🔗 LinkedIn : SWA Tech & Meyan Traoré<br>" +
        "📍 Basée à Paris, disponible en France & Afrique francophone",
      choices: [
        { label: "💬 Ouvrir WhatsApp", href: CONTACT.whatsapp },
        { label: "📧 Envoyer un email", href: "mailto:" + CONTACT.email },
        { label: "📅 Prendre rendez-vous", next: "rdv" },
        { label: "📨 Page Contact complète", href: "contact.html" },
        { label: "⬅️ Retour au menu", next: "root" },
      ],
    },
  };

  /* ---------- Construction de l'interface ---------- */

  function init() {
    const launcher = document.createElement("button");
    launcher.id = "swa-chat-launcher";
    launcher.type = "button";
    launcher.setAttribute("aria-label", "Ouvrir l'assistant SWA Tech");
    launcher.innerHTML = "💬";

    const panel = document.createElement("div");
    panel.id = "swa-chat-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Assistant SWA Tech");
    panel.innerHTML =
      '<div class="swa-chat-header">' +
      '  <div class="swa-chat-title">' +
      '    <span class="swa-chat-badge">🛡️</span>' +
      '    <div><strong>Assistant SWA Tech</strong><br><small>Réponses instantanées</small></div>' +
      "  </div>" +
      '  <button type="button" class="swa-chat-close" aria-label="Fermer l\'assistant">✕</button>' +
      "</div>" +
      '<div class="swa-chat-body" id="swa-chat-body"></div>';

    const bubble = document.createElement("div");
    bubble.id = "swa-chat-bubble";
    bubble.innerHTML =
      '<button type="button" class="swa-chat-bubble-close" aria-label="Fermer le message">✕</button>' +
      '<p>👋 Bonjour ! SWA Tech est là pour vous aider et répondre à vos questions.</p>';

    document.body.appendChild(launcher);
    document.body.appendChild(panel);
    document.body.appendChild(bubble);

    const body = panel.querySelector("#swa-chat-body");
    const closeBtn = panel.querySelector(".swa-chat-close");
    const bubbleClose = bubble.querySelector(".swa-chat-bubble-close");

    setTimeout(() => bubble.classList.add("show"), 900);

    function hideBubble() {
      bubble.classList.remove("show");
    }

    bubble.addEventListener("click", (e) => {
      if (e.target === bubbleClose) {
        hideBubble();
        return;
      }
      hideBubble();
      openPanel();
    });

    function openPanel() {
      panel.classList.add("open");
      if (!body.dataset.started) {
        body.dataset.started = "1";
        renderNode("root", false);
      }
    }

    launcher.addEventListener("click", () => {
      hideBubble();
      panel.classList.toggle("open");
      if (panel.classList.contains("open") && !body.dataset.started) {
        body.dataset.started = "1";
        renderNode("root", false);
      }
    });
    closeBtn.addEventListener("click", () => panel.classList.remove("open"));

    function addBotMessage(html) {
      const msg = document.createElement("div");
      msg.className = "swa-chat-msg swa-chat-bot";
      msg.innerHTML = html;
      body.appendChild(msg);
      scrollToBottom();
    }

    function addUserMessage(text) {
      const msg = document.createElement("div");
      msg.className = "swa-chat-msg swa-chat-user";
      msg.textContent = text;
      body.appendChild(msg);
      scrollToBottom();
    }

    function clearChoices() {
      const old = body.querySelector(".swa-chat-choices");
      if (old) old.remove();
    }

    function renderNode(nodeId, userClicked) {
      const node = TREE[nodeId];
      if (!node) return;
      clearChoices();
      addBotMessage(node.message);

      const choicesWrap = document.createElement("div");
      choicesWrap.className = "swa-chat-choices";

      node.choices.forEach((choice) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "swa-chat-choice";
        btn.textContent = choice.label;
        btn.addEventListener("click", () => {
          addUserMessage(choice.label);
          if (choice.href) {
            choicesWrap.remove();
            const link = document.createElement("div");
            link.className = "swa-chat-msg swa-chat-bot";
            link.innerHTML =
              '<a class="swa-chat-link" href="' +
              choice.href +
              '" target="' +
              (choice.href.startsWith("http") || choice.href.startsWith("mailto") ? "_blank" : "_self") +
              '" rel="noopener">Ouvrir →</a>';
            body.appendChild(link);
            scrollToBottom();
            if (choice.next) {
              setTimeout(() => renderNode(choice.next, true), 150);
            } else {
              setTimeout(() => renderNode("root", true), 600);
            }
          } else if (choice.next) {
            choicesWrap.remove();
            setTimeout(() => renderNode(choice.next, true), 150);
          }
        });
        choicesWrap.appendChild(btn);
      });

      body.appendChild(choicesWrap);
      scrollToBottom();
    }

    function scrollToBottom() {
      body.scrollTop = body.scrollHeight;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
