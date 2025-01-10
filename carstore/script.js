document.addEventListener("DOMContentLoaded", () => {
    // Placeholder for functionality
    console.log("Autokauppa loaded.");
    
    // Example login
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        if (username === "admin" && password === "password") {
          window.location.href = "panel.html";
        } else {
          alert("Väärä käyttäjänimi tai salasana.");
        }
      });
    }
  
    // Placeholder to load JSON data and render it in pages
  });

  document.addEventListener("DOMContentLoaded", () => {
    const adminCarList = document.getElementById("adminCarList");
    const carList = document.getElementById("carList");
    const filterInput = document.getElementById("filterInput");
  
    // Lataa autot JSON-tiedostosta
    fetch("data.json")
      .then((response) => response.json())
      .then((data) => {
        const cars = data.cars;
  
        // Näytä autot adminille
        if (adminCarList) {
          adminCarList.innerHTML = cars.map(car => `
            <div class="car">
              <h3>${car.make} ${car.model} (${car.year})</h3>
              <p>Hinta: €${car.price}</p>
              <button onclick="editCar(${car.id})">Muokkaa</button>
            </div>
          `).join("");
        }
  
        // Näytä autot käyttäjille
        if (carList) {
          renderCarList(cars);
  
          // Rajaa hakutuloksia
          filterInput.addEventListener("input", () => {
            const filterText = filterInput.value.toLowerCase();
            const filteredCars = cars.filter(car => 
              car.make.toLowerCase().includes(filterText) ||
              car.model.toLowerCase().includes(filterText) ||
              car.year.toString().includes(filterText)
            );
            renderCarList(filteredCars);
          });
        }
      });
  
    // Renderöi autolista cars.html-sivulle
    function renderCarList(cars) {
      carList.innerHTML = cars.map(car => `
        <div class="car">
          <h3>${car.make} ${car.model} (${car.year})</h3>
          <p>Hinta: €${car.price}</p>
          <a href="carinfo.html?id=${car.id}">Näytä tiedot</a>
        </div>
      `).join("");
    }
  });
  
  // Muokkaa auton tietoja
  function editCar(id) {
    window.location.href = `edit.html?id=${id}`;
  }
  