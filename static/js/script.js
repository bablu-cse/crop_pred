// Add this to your existing script.js file

// Update the form submission handler
document.getElementById('prediction-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        temperature: temperatureInput.value,
        humidity: humidityInput.value,
        ph: phInput.value,
        water_availability: waterInput.value,
        season: seasonSelect.value
    };
    
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('crop-name').textContent = data.crop;
            document.getElementById('confidence').textContent = `Confidence: ${data.confidence}%`;
            document.getElementById('result').style.display = 'block';
            
            // NEW: Update roadmap link
            const roadmapLink = document.getElementById('roadmap-link');
            roadmapLink.href = `/roadmap/${encodeURIComponent(data.crop)}`;
            document.getElementById('roadmap-action').style.display = 'block';
            
            // Store user input for potential use in roadmap
            sessionStorage.setItem('userInput', JSON.stringify(data.user_input));
            
            // Scroll to results
            document.getElementById('result').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center'
            });
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});