// Mock data for demonstration
const soilListings = [
    { id: 1, type: "Loamy", quantity: 100, price: 50, location: "Springfield" },
    { id: 2, type: "Sandy", quantity: 200, price: 30, location: "Greenfield" },
];

// Render listings
function renderListings(listings) {
    const listingsSection = document.querySelector('.listings');
    listingsSection.innerHTML = ""; // Clear previous content
    listings.forEach(listing => {
        const listingCard = `
            <div class="listing-card">
                <h3>${listing.type} Soil</h3>
                <p>Quantity: ${listing.quantity}kg</p>
                <p>Price: $${listing.price}</p>
                <p>Location: ${listing.location}</p>
                <button class="btn">Contact Seller</button>
            </div>`;
        listingsSection.innerHTML += listingCard;
    });
}

// Filter logic
document.getElementById('filterForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const typeFilter = document.getElementById('soilType').value.toLowerCase();
    const filteredListings = soilListings.filter(listing => 
        (typeFilter === 'all' || listing.type.toLowerCase() === typeFilter)
    );
    renderListings(filteredListings);
});

// Initial render
renderListings(soilListings);
