// Sample data
let myPackages = [
    { id: 1, description: "Package 1", pickupAddress: "123 Main St", status: "In transit", notes: "Fragile item" },
    { id: 2, description: "Package 2", pickupAddress: "456 Elm St", status: "Delivered", notes: "Handle with care" },
    { id: 3, description: "Package 3", pickupAddress: "789 Oak St", status: "Pending", notes: "" },
];

let myPickups = [
    { id: 4, description: "Package 4", deliveryAddress: "987 Pine St", status: "Scheduled", notes: "Large package" },
    { id: 5, description: "Package 5", deliveryAddress: "654 Maple St", status: "In progress", notes: "" },
];

// Display my packages
function displayMyPackages() {
    // Remove active class from all buttons
    document.getElementById("myPackagesTab").classList.add("active");
    document.getElementById("myPickupsTab").classList.remove("active");

    const packageList = document.getElementById("packageList");
    packageList.innerHTML = "";

    for (const package of myPackages) {
        const listItem = document.createElement("a");
        listItem.href = "#";
        listItem.className = "list-group-item list-group-item-action flex-column align-items-start";
        listItem.addEventListener("click", () => togglePackageDetails(listItem, package));

        const itemContent = `
      <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1">${package.description}</h5>
        <small>${package.status}</small>
      </div>
      <p class="mb-1">Package ID: ${package.id}</p>
      <div class="package-details" style="display: none;">
        <br>
        <p>Pickup Address: ${package.pickupAddress}</p>
        <p>Delivery Address: ${package.deliveryAddress}</p>
        <p>Instructions: ${package.notes}</p>
      </div>
      <button class="btn btn-success btn-sm" onclick="markPackageReceived(${package.id}); removePackageItem(${package.id})">Received</button>
    `;

        listItem.innerHTML = itemContent;
        packageList.appendChild(listItem);
    }
}

// Display my pickups
function displayMyPickups() {
    // Remove active class from all buttons
    document.getElementById("myPackagesTab").classList.remove("active");
    document.getElementById("myPickupsTab").classList.add("active");

    const packageList = document.getElementById("packageList");
    packageList.innerHTML = "";

    for (const package of myPickups) {
        const listItem = document.createElement("a");
        listItem.href = "#";
        listItem.className = "list-group-item list-group-item-action flex-column align-items-start";
        listItem.addEventListener("click", () => togglePackageDetails(listItem, package));

        const itemContent = `
      <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1">${package.description}</h5>
        <small>${package.status}</small>
      </div>
      <p class="mb-1">Package ID: ${package.id}</p>
      <div class="package-details" style="display: none;">
        <p>Pickup Address: ${package.pickupAddress}</p>
        <p>Delivery Address: ${package.deliveryAddress}</p>
        <p>Instructions: ${package.notes}</p>
      </div>
      <button class="btn btn-primary btn-sm" onclick="markPackageDelivered(${package.id}); removePackageItem(${package.id})">Delivered</button>
    `;

        listItem.innerHTML = itemContent;
        packageList.appendChild(listItem);
    }
}

// Toggle the display of package details
function togglePackageDetails(listItem, package) {
    const details = listItem.querySelector(".package-details");
    if (event.target.tagName !== "BUTTON") {
        details.style.display = details.style.display === "none" ? "block" : "none";
    }
}

// Remove package item from the list
function removePackageItem(packageId) {
    // Find and remove the package item from the corresponding list
    myPackages = myPackages.filter((package) => package.id !== packageId);
    myPickups = myPickups.filter((package) => package.id !== packageId);

    // Redisplay the packages based on the active tab
    const myPackagesTab = document.getElementById("myPackagesTab");
    if (myPackagesTab.classList.contains("active")) {
        displayMyPackages();
    } else {
        displayMyPickups();
    }
}

// Mark package as received
function markPackageReceived(packageId) {
    // Update the package status in the database (replace with your own logic)
    console.log(`Package ${packageId} marked as received`);
}

// Mark package as delivered
function markPackageDelivered(packageId) {
    // Update the package status in the database (replace with your own logic)
    console.log(`Package ${packageId} marked as delivered`);
}

// Initialize the page
function initializePage() {
    displayMyPackages();
}

// Event listeners for tab clicks
document.getElementById("myPackagesTab").addEventListener("click", displayMyPackages);
document.getElementById("myPickupsTab").addEventListener("click", displayMyPickups);

// Initialize the page when the DOM is loaded
document.addEventListener("DOMContentLoaded", initializePage);
