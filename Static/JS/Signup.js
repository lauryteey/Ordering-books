// Funksjon for å vise meldinger
function showMessage(inputId, message, color = "red") {
    const messageElement = document.getElementById(`${inputId}-error`); // Henter elementet for feilmelding
    if (messageElement) {
        messageElement.textContent = message; // Setter meldingsteksten
        messageElement.style.color = color;  // Angir fargen på meldingen
        messageElement.style.paddingTop = "10px"; // Legger avstand mellom inputfeltet og feilmeldingen
        messageElement.style.paddingBottom = "10px"; // Legger avstand på bunnen
    }
}

// Legger til en submit-hendelse for skjemaet
document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Hindrer standard last ned (reload av siden)

    // Rydder meldinger før innsending
    document.querySelectorAll(".error-message").forEach(msg => (msg.textContent = ""));

    // Henter verdier fra inputfeltene
    const formData = {
        fornavn: document.getElementById("first-name").value.trim(), // Henter fornavn
        e_post: document.getElementById("email").value.trim(), // Henter e-post
        passord: document.getElementById("password").value // Henter passord
    };

    // Email validering med regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const gyldigDomener = ["gmail.com", "example.com", "yahoo.com"]; // Gyldige domener for e-post

    const emailParts = formData.e_post.split("@"); // Deler opp e-post i deler
    const domain = emailParts.length > 1 ? emailParts[1] : null; // Henter domenet fra e-post

    let hasError = false; // Setter flagg for om det finnes feil

    // Feilmeldinger for ugyldig e-post
    if (!emailRegex.test(formData.e_post)) {
        showMessage("email", "Ugyldig e-postformat"); // Viser feilmelding
        hasError = true;
    }

    if (!gyldigDomener.includes(domain)) {
        showMessage("email", "Vennligst bruk en gyldig e-postdomene."); // Feil domenenavn
        hasError = true;
    }

    // Validere passordet
    const password = formData.passord;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordRegex.test(password)) {
        alert("Passordet må være minst 8 tegn og inneholde minst én stor bokstav, én liten bokstav, ett tall, og ett spesialtegn."); // Passordregler
        return; // Stopper hvis passordet er ugyldig
    }

    if (!formData.fornavn) {
        showMessage("first-name", "Fornavn er påkrevd."); // Feilmelding hvis fornavn mangler
        hasError = true;
    }

    if (hasError) return; // Stopper funksjonen hvis det er feil

    try {
        // Sender data til serveren for å opprette bruker
        const response = await fetch("/create_user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (response.ok) { // Hvis brukeren ble opprettet
            alert("Brukeren ble opprettet!");
            window.location.href = "/"; // Går til hovedsiden etter vellykket registrering
        } else if (result.error === "email_exists") {
            console.log(result.error);
            showMessage("email", "E-postadressen er allerede registrert."); // Feilmelding hvis e-post allerede finnes
            hasError = true;
        } else {
            showMessage(result.error || "Kunne ikke opprette bruker."); // Vis annen feilmelding
        }
    } catch (error) {
        console.error("Feil under opprettelse av bruker:", error);
        alert("En feil oppsto. Vennligst prøv igjen."); // Feilmelding hvis det skjer noe med serveren
    }
});
