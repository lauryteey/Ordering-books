function showMessage(id, message, color = "green") {
    const messageElement = document.getElementById(id);
    if (messageElement) {
        messageElement.textContent = message; // Setter meldingen i elementet
        messageElement.style.color = color;  // Endrer tekstfargen til den som er spesifisert
        messageElement.style.paddingTop = "10px"; // Legger til litt plass øverst
        messageElement.style.paddingBottom = "10px"; // Legger til litt plass nederst
    }
}

// Når skjemaet blir sendt (submit)
document.getElementById('bestillingForm').addEventListener('submit', async function (e) {
    console.log("Knappen ble trykket");
    e.preventDefault(); // Stopper at siden lastes på nytt når skjemaet sendes

    // Fjerner eventuelle tidligere feilmeldinger før skjemaet sendes
    document.querySelectorAll(".error-message").forEach(msg => (msg.textContent = ""));

    // Henter verdiene fra inputfeltene og fjerner eventuelle ekstra mellomrom
    const translate_from = document.getElementById('translate_from').value.trim();
    const translate_to = document.getElementById('translate_to').value.trim();
    const delivery_time = document.getElementById('delivery_time').value; // Henter leveringsdatoen
    const description = document.getElementById('description').value.trim(); // Henter beskrivelsen

    // Lager et objekt med all informasjonen som skal sendes
    const data = {
        translate_from: translate_from,
        translate_to: translate_to,
        delivery_time: delivery_time,
        description: description
    };

    console.log(data); // Skriver ut dataene i konsollen for å se hva som blir sendt

    let hasError = false; // Variabel for å sjekke om det er noen feil

    // Hvis det er en feil, stopper vi videre behandling 
    if (hasError) return;

    try {
        // Sender en POST-forespørsel til serveren med skjema-dataene som JSON
        const response = await fetch("/bestilling", {
            method: "POST", // Bruker POST-metoden for å sende data
            headers: { "Content-Type": "application/json" }, // Sender data som JSON
            body: JSON.stringify(data), // Konverterer data til JSON-format
        });

        // Venter på svar fra serveren og parser det som JSON
        const result = await response.json();

        if (result.error) {
            // Hvis det er en feil i svaret, viser det feilmeldingen
            showMessage("message", result.error, "red"); 
            console.log(result.error); // Skriver ut feilmeldingen i konsollen
        } else {
            // Hvis alt gikk bra, går brukeren til bekreftelsessiden
            window.location.href = "/bekreftelse"; // Erstatt med riktig URL for bekreftelsessiden
        }
    } catch (error) {
        // Hvis det oppstår en feil under forespørselen 
        console.error("Feil under sending av bestillingen", error); // Skriver ut feilen i konsollen
        showMessage("message", "En feil oppsto. Vennligst prøv igjen.", "red"); // Vist generell feilmelding 
    }

});
