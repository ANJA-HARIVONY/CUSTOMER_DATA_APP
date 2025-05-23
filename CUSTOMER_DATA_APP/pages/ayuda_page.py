import reflex as rx

def ayuda_page():
    """Create a fun and intuitive help page with emojis."""
    return rx.center(
        rx.vstack(
            rx.heading("🤝 Bienvenue dans l'Aide de Conexxia!", size="6", margin_bottom="1em", text_align="center"),
            
            # Section principale
            rx.vstack(
                rx.heading("📚 Guide Rapide", size="4", margin_bottom="1em", text_align="center"),
                rx.text("Voici comment utiliser notre application:", size="4", text_align="center"),
                
                # Cartes d'aide
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text("📊 Dashboard", size="4", weight="bold", text_align="center"),
                            rx.text("Visualisez toutes vos statistiques importantes en un coup d'œil!", size="3", text_align="center"),
                            rx.text("• Total des incidencias", size="3", text_align="center"),
                            rx.text("• Incidencias en attente", size="3", text_align="center"),
                            rx.text("• Incidencias résolues", size="3", text_align="center"),
                            padding="1em",
                            border_radius="lg",
                            background_color=rx.color("blue", 3),
                            width="300px",
                            transition="all 0.2s",
                            _hover={"transform": "scale(1.05)"},
                        ),
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("🔧 Service", size="4", weight="bold", text_align="center"),
                            rx.text("Gérez vos services et suivez leur progression!", size="3", text_align="center"),
                            rx.text("• Créer un nouveau service", size="3", text_align="center"),
                            rx.text("• Suivre les services en cours", size="3", text_align="center"),
                            rx.text("• Historique des services", size="3", text_align="center"),
                            padding="1em",
                            border_radius="lg",
                            background_color=rx.color("green", 3),
                            width="300px",
                            transition="all 0.2s",
                            _hover={"transform": "scale(1.05)"},
                        ),
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("📈 Données", size="4", weight="bold", text_align="center"),
                            rx.text("Accédez à toutes vos données en temps réel!", size="3", text_align="center"),
                            rx.text("• Tableau de données complet", size="3", text_align="center"),
                            rx.text("• Filtres et recherche", size="3", text_align="center"),
                            rx.text("• Export en CSV", size="3", text_align="center"),
                            padding="1em",
                            border_radius="lg",
                            background_color=rx.color("orange", 3),
                            width="300px",
                            transition="all 0.2s",
                            _hover={"transform": "scale(1.05)"},
                        ),
                    ),
                    spacing="4",
                    width="100%",
                    justify="center",
                    wrap="wrap",
                ),
                
                # Section FAQ
                rx.vstack(
                    rx.heading("❓ Questions Fréquentes", size="4", margin_top="2em", margin_bottom="1em", text_align="center"),
                    rx.accordion.root(
                        rx.accordion.item(
                            rx.accordion.trigger("Comment ajouter une nouvelle incidencia? 🤔"),
                            rx.accordion.content(
                                "Cliquez sur le bouton '+' en haut à droite du tableau. Remplissez le formulaire et cliquez sur 'Ajouter incidencia'."
                            ),
                        ),
                        rx.accordion.item(
                            rx.accordion.trigger("Comment modifier une incidencia? ✏️"),
                            rx.accordion.content(
                                "Cliquez sur l'icône de crayon à côté de l'incidencia que vous souhaitez modifier. Modifiez les informations et cliquez sur 'Actualizar'."
                            ),
                        ),
                        rx.accordion.item(
                            rx.accordion.trigger("Comment supprimer une incidencia? 🗑️"),
                            rx.accordion.content(
                                "Cliquez sur l'icône de corbeille à côté de l'incidencia que vous souhaitez supprimer. Confirmez la suppression."
                            ),
                        ),
                        rx.accordion.item(
                            rx.accordion.trigger("Comment exporter les données? 📤"),
                            rx.accordion.content(
                                "Cliquez sur l'icône de téléchargement dans le pied de page. Les données seront exportées au format CSV."
                            ),
                        ),
                        type="single",
                        collapsible=True,
                        width="100%",
                        max_width="800px",
                    ),
                ),
                
                # Section Contact
                rx.vstack(
                    rx.heading("📞 Besoin d'aide supplémentaire?", size="4", margin_top="2em", margin_bottom="1em", text_align="center"),
                    rx.text("Contactez notre équipe de support:", size="4", text_align="center"),
                    rx.hstack(
                        rx.icon("mail", size=24),
                        rx.link(
                            "jefe.incidencias@conexxiaeg.com",
                            href="mailto:jefe.incidencias@conexxiaeg.com",
                            color=rx.color("blue", 9),
                        ),
                        spacing="2",
                        justify="center",
                    ),
                    rx.hstack(
                        rx.icon("phone", size=24),
                        rx.text("222 304 981", size="4"),
                        spacing="2",
                        justify="center",
                    ),
                    padding="2em",
                    border_radius="lg",
                    background_color=rx.color("gray", 2),
                    width="100%",
                    max_width="800px",
                ),
                
                spacing="4",
                width="100%",
                padding="2em",
                align_items="center",
            ),
            
            width="100%",
            max_width="1200px",
            padding="2em",
            align_items="center",
        ),
        width="100%",
    )