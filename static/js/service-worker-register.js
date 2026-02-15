// Register service worker for PWA functionality

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered successfully:', registration.scope);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// Handle install prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Save the event for later use
    deferredPrompt = e;
    // Show install button (you can add this to your UI)
    showInstallPromotion();
});

function showInstallPromotion() {
    // You can create a custom install button in your UI
    console.log('PWA installation available');
}

// Handle app installed
window.addEventListener('appinstalled', () => {
    console.log('Naija Connect PWA installed successfully');
    deferredPrompt = null;
});
