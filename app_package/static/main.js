
// asynchronous programming using fetch to update remaining capacity

document.addEventListener("DOMContentLoaded", () => {
    const remainingSpan = document.getElementById("remaining-capacity");
    if (remainingSpan) {
        const eventId = remainingSpan.getAttribute("data-event-id");
        
        async function updateRemaining() {
            try {
                const response = await fetch(`/api/events/${eventId}/remaining`);
                if (!response.ok) return;
                const data = await response.json();
                remainingSpan.textContent = data.remaining_capacity;
            } catch (err) {
                console.error("Error fetching remaining capacity", err);
            }
        }

        updateRemaining();
        setInterval(updateRemaining, 10000);
    }
});
