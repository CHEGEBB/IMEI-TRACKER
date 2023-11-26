function trackDevice() {
    var imei = document.getElementById('imeiInput').value;

    // Use jQuery for simplicity, you can use other methods like fetch
    $.get(`/track?imei=${imei}`, function(response) {
        console.log(response);
    });
}
