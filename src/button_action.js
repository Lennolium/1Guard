const API_ACCESS_KEY = "8a6e875fc0c936c9728f03e8cab86c7bd7845a08f63eb623ac04a4b89dbf369f";
const API_LOGIN_URL = 'https://oneguard-server.onrender.com/auth/login';
const API_ANALYZE_URL = 'https://oneguard-server.onrender.com/analyze/ask';
const API_FEEDBACK_URL = 'https://oneguard-server.onrender.com/analyze/feedback';
var currentUrl = ""

function generateRandomId() {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0];
}

function api_login() {

    const username = generateRandomId()
    var password = CryptoJS.SHA256(API_ACCESS_KEY).toString(CryptoJS.enc.Hex);
    const base64Credentials = btoa(`${username}:${password}`);
    return fetch(API_LOGIN_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64Credentials
        },
    }).then(response => {
        if (!response.ok) {
            throw new Error("HTTP status " + response.status);
        }
        return response.json();
    }).then(data => {
        const token = data.token;
        return token

    })
}

// Function to fetch a new token initially and schedule subsequent refreshes
async function refreshTokenEveryHour() {
    // Fetch a new token initially
    let token = await api_login();

    // Schedule token refresh every hour
    setInterval(async () => {
        token = await api_login();
    }, 60 * 60 * 1000); // 1 hour in milliseconds
    return token;
}

function api_analyze(data, token) {
    const headers = {'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`}
        return fetch(API_ANALYZE_URL, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data)
        }).then(response => {
            if (!response.ok) {
                throw new Error("HTTP status " + response.status);
            }
            return response.json();
        })
}

function api_feedback(data, token) {
    const headers_feedback = {'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`}
    return fetch(API_FEEDBACK_URL, {
        method: 'POST',
        headers: headers_feedback,
        body: JSON.stringify(data)
    }).then(response => {
        if (!response.ok) {
            throw new Error("HTTP status " + response.status);
        }
        if (response.ok) {
            console.log("HTTP status code 200!")
        }
        return response.json();
    })

}
// code loaded into DOM event so it doesn't run first
document.addEventListener('DOMContentLoaded', async function() { 
    let tokens = await refreshTokenEveryHour()

    var trusted_button = document.getElementById("trusted")

    function updateCurrentUrl() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        currentUrl = tabs[0].url;
        var domain_split = currentUrl.split('/')
        var domain_only = domain_split[2]
        document.getElementById('current-url').textContent = domain_only;
        });
    }
    updateCurrentUrl()

    async function trusted_action() {
        var data_trust = {'domain': currentUrl, "user_feedback": "trust"}
        await api_feedback(data_trust, tokens)
        alert("thank you for your feedback !")
    }
    trusted_button.addEventListener("click", trusted_action) // when trusted button is clicked

    var scam_button = document.getElementById("scamm")
    async function scam_action() {
        var data_scam = {'domain': currentUrl, "user_feedback": "scam"}
        await api_feedback(data_scam, tokens) 
        alert("thank you for your feedback !")
    }
    scam_button.addEventListener("click", scam_action) // when scam button is clicked

    var detailed_button = document.getElementById("detail")
    async function detailed_action() {
        var data_domain = {'domain': currentUrl}
        var end_score = await api_analyze(data_domain, tokens) 
        alert("Please wait while the shop's score is generated")
        var displayed_score = document.createElement('button');
        var stringified_score = JSON.stringify(end_score);
        var jsonobj = JSON.parse(stringified_score);
        var end_score = jsonobj.score;
        var color;
        if (end_score == "1") {
            color = 'red';
            end_score = "F-";

        } else if (end_score == "2") {
            color = 'red';
            end_score = "F";

        } else if (end_score == "3") {
            color = 'red';
            end_score = "F+";

        } else if (end_score == "4") {
            color = 'orange';
            end_score = "D-"

        } else if (end_score == "5") {
            color = 'orange'; 
            end_score = "D"
        } else if (end_score == "6") {
            color = 'orange';
            end_score = "D+";

        } else if (end_score == "7") {
            color = 'yellow';
            end_score = "C-";

        } else if (end_score == "8") {
            color = 'yellow';
            end_score = "C";

        } else if (end_score == "9") {
            color = 'yellow';
            end_score = "C+"

        } else if (end_score == "10") {
            color = 'Light green'; 
            end_score = "B-"
        } else if (end_score == "11") {
            color = 'Light green';
            end_score = "B";

        } else if (end_score == "12") {
            color = 'Light Green';
            end_score = "B+";

        } else if (end_score == "13") {
            color = 'green';
            end_score = "A-";

        } else if (end_score == "14") {
            color = 'green';
            end_score = "A"

        } else if (end_score == "15") {
            color = 'green'; 
            end_score = "A+"
        }

        displayed_score.textContent = end_score;
        displayed_score.style.color = 'white';
        displayed_score.style.backgroundColor = color;
        displayed_score.style.fontSize = "40px";
        detailed_button.parentNode.insertBefore(displayed_score, detailed_button.nextSibling);
        setTimeout(function() {
            displayed_score.remove();
        }, 20000);
    }
    detailed_button.addEventListener("click", detailed_action) // when generate score button is clicked

})
