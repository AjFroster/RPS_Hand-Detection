


function sendGesture(gesture) {
    console.log("sendGesture in javascript sees"+gesture)
    fetch('/handle_gesture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ gesture: gesture })
    })
    .then(response => response.json())
    .then(data => {
        // Update your webpage based on the response
        console.log(data);
        document.getElementById('result').innerText = data.result;
        document.getElementById('user_score').innerText = data.user_score;
        document.getElementById('computer_score').innerText = data.computer_score;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
