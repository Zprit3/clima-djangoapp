document.getElementById('show-local-temp').addEventListener('click', function() {
    const apiKey = document.getElementById('api-key').value;

    navigator.geolocation.getCurrentPosition(function(position) {
        let apiUrl = `http://api.openweathermap.org/data/2.5/weather?lat=${position.coords.latitude}&lon=${position.coords.longitude}&appid=${apiKey}&units=metric&lang=es`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                let temperaturaLocal = data.main.temp;
                document.getElementById('local-temp').textContent = temperaturaLocal + '°C';
            })
            .catch(error => console.error("Error fetching weather data:", error));
    }, error => console.error("Error getting location:", error));
});