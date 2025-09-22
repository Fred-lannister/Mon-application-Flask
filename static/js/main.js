// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des graphiques (Chart.js)
    const expensesCtx = document.getElementById('expensesChart');
    const balanceCtx = document.getElementById('balanceChart');
    const monthlyExpensesBarCtx = document.getElementById('monthlyChart');

    // Graphique en secteurs des dépenses
    if (expensesCtx) {
        new Chart(expensesCtx, {
            type: 'pie',
            data: {
                labels: expensesLabels,
                datasets: [{
                    label: 'Dépenses par catégorie',
                    data: expensesValues,
                    backgroundColor: ['#0d6efd', '#dc3545', '#ffc107', '#198754', '#6610f2', '#fd7e14', '#e83e8c', '#6f42c1'],
                    hoverOffset: 4
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#333'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff'
                    }
                }
            }
        });
    }

    // Graphique d'évolution du solde
    if (balanceCtx) {
        new Chart(balanceCtx, {
            type: 'line',
            data: {
                labels: balanceLabels,
                datasets: [{
                    label: 'Évolution du solde',
                    data: balanceValues,
                    fill: true,
                    borderColor: '#0d6efd',
                    tension: 0.3,
                    backgroundColor: 'rgba(13, 110, 253, 0.2)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Solde (FCFA)'
                        }
                    }
                }
            }
        });
    }

    // NOUVEAU: Graphique des dépenses mensuelles
    if (monthlyExpensesBarCtx) {
        new Chart(monthlyExpensesBarCtx, {
            type: 'bar',
            data: {
                labels: monthlyExpensesLabels,
                datasets: [{
                    label: 'Dépenses mensuelles',
                    data: monthlyExpensesValues,
                    backgroundColor: '#dc3545',
                    borderColor: '#c98087ff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // GESTION DES BOUTONS DE GÉNÉRATION ET D'EFFACEMENT DE DONNÉES
    function customDialog(message, isConfirm = false, callback = null) {
        // Supprimer tout dialogue existant
        const existingDialog = document.getElementById('custom-dialog');
        if (existingDialog) {
            existingDialog.remove();
        }

        // Créer les éléments du dialogue
        const dialog = document.createElement('div');
        dialog.id = 'custom-dialog';
        dialog.classList.add('dialog-overlay');
        
        dialog.innerHTML = `
            <div class="dialog-content">
                <p>${message}</p>
                <div class="dialog-buttons">
                    <button id="okBtn">OK</button>
                    ${isConfirm ? '<button id="cancelBtn">Annuler</button>' : ''}
                </div>
            </div>
        `;
        
        document.body.appendChild(dialog);
        
        // Ajouter un style basique pour le dialogue
        const style = document.createElement('style');
        style.textContent = `
            .dialog-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .dialog-content {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 90%;
                text-align: center;
            }
            .dialog-buttons {
                margin-top: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;
            }
            .dialog-buttons button {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            #okBtn {
                background-color: #0d6efd;
                color: #fff;
            }
            #cancelBtn {
                background-color: #6c757d;
                color: #fff;
            }
        `;
        document.head.appendChild(style);

        // Gérer les clics sur les boutons
        document.getElementById('okBtn').addEventListener('click', () => {
            dialog.remove();
            style.remove();
            if (callback) {
                callback();
            }
        });

        if (isConfirm) {
            document.getElementById('cancelBtn').addEventListener('click', () => {
                dialog.remove();
                style.remove();
            });
        }
    }

    const generateDataBtn = document.getElementById('generate-data-btn');
    if (generateDataBtn) {
        generateDataBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            customDialog('Êtes-vous sûr de vouloir générer des données de test ? Cela effacera toutes les transactions existantes.', true, () => {
                fetch('/generate-data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                })
                .then(response => response.json())
                .then(data => {
                    customDialog(data.message);
                    window.location.reload();
                })
                .catch((error) => {
                    console.error('Erreur:', error);
                    customDialog('Une erreur est survenue lors de la génération des données.');
                });
            });
        });
    }

    const clearDataBtn = document.getElementById('clear-data-btn');
    if (clearDataBtn) {
        clearDataBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            customDialog('Êtes-vous sûr de vouloir effacer TOUTES vos transactions ? Cette action est irréversible.', true, () => {
                fetch('/clear-data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                })
                .then(response => response.json())
                .then(data => {
                    customDialog(data.message);
                    window.location.reload();
                })
                .catch((error) => {
                    console.error('Erreur:', error);
                    customDialog('Une erreur est survenue lors de l\'effacement des données.');
                });
            });
        });
    }

    // GESTION DU CHAT
    const chatForm = document.getElementById('chat-form');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender, 'mb-3', 'p-3', 'rounded');
        messageDiv.innerHTML = text;
        
        if (sender === 'sent') {
            messageDiv.classList.add('bg-primary', 'text-white', 'align-self-end');
        } else {
            messageDiv.classList.add('bg-light-subtle', 'align-self-start');
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = userInput.value.trim();
            if (message === '') return;
            addMessage(message, 'sent');
            userInput.value = '';

            fetch('/chat_api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'message': message })
            })
            .then(response => response.json())
            .then(data => addMessage(data.response, 'received'))
            .catch(error => {
                console.error('Erreur:', error);
                addMessage('Désolé, une erreur est survenue. Veuillez vérifier votre clé API.', 'received');
            });
        });
    }
});

