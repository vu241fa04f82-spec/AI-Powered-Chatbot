const chatBox = document.getElementById("chat-box");

const messageInput =
    document.getElementById("message-input");

const sendButton =
    document.getElementById("send-button");


function addMessage(message, sender) {

    const messageDiv =
        document.createElement("div");

    messageDiv.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );


    const contentDiv =
        document.createElement("div");

    contentDiv.classList.add("message-content");

    contentDiv.textContent = message;


    messageDiv.appendChild(contentDiv);

    chatBox.appendChild(messageDiv);


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (message === "") {
        return;
    }


    addMessage(message, "user");


    messageInput.value = "";

    sendButton.disabled = true;


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });


        const data =
            await response.json();


        addMessage(
            data.response,
            "bot"
        );


    } catch (error) {

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        console.error(error);

    }


    sendButton.disabled = false;

    messageInput.focus();
}


function sendSuggestion(message) {

    messageInput.value = message;

    sendMessage();

}


sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keypress",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);