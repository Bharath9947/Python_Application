from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# -------------------------------------------------------------------
# Demo flight data
# -------------------------------------------------------------------
FLIGHTS = [
    {
        "id": 1, "airline": "IndiGo", "logo": "🟦", "number": "6E 2053",
        "from": "HYD", "from_city": "Hyderabad", "to": "DEL",
        "to_city": "Delhi", "departure": "06:10", "arrival": "08:35",
        "duration": "2h 25m", "price": 4899, "tag": "Non-stop"
    },
    {
        "id": 2, "airline": "Air India", "logo": "🔴", "number": "AI 542",
        "from": "HYD", "from_city": "Hyderabad", "to": "DEL",
        "to_city": "Delhi", "departure": "09:20", "arrival": "11:50",
        "duration": "2h 30m", "price": 5799, "tag": "Free meal"
    },
    {
        "id": 3, "airline": "Vistara", "logo": "🟣", "number": "UK 897",
        "from": "HYD", "from_city": "Hyderabad", "to": "DEL",
        "to_city": "Delhi", "departure": "14:15", "arrival": "16:40",
        "duration": "2h 25m", "price": 6299, "tag": "Extra legroom"
    },
    {
        "id": 4, "airline": "IndiGo", "logo": "🟦", "number": "6E 611",
        "from": "HYD", "from_city": "Hyderabad", "to": "DEL",
        "to_city": "Delhi", "departure": "19:30", "arrival": "21:55",
        "duration": "2h 25m", "price": 5199, "tag": "Non-stop"
    }
]

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SkyBook — Flight Booking</title>

<style>
*{box-sizing:border-box;margin:0;padding:0}

:root{
 --primary:#2563eb;
 --primary-dark:#1d4ed8;
 --accent:#06b6d4;
 --dark:#0f172a;
 --text:#334155;
 --muted:#64748b;
 --light:#f8fafc;
 --border:#e2e8f0;
 --white:#fff;
 --success:#16a34a;
 --shadow:0 15px 40px rgba(15,23,42,.08)
}

body{
 font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
 background:#f1f5f9;
 color:var(--dark)
}

.navbar{
 height:74px;background:rgba(255,255,255,.92);
 backdrop-filter:blur(16px);
 border-bottom:1px solid rgba(226,232,240,.8);
 display:flex;align-items:center;justify-content:space-between;
 padding:0 6%;position:sticky;top:0;z-index:100
}

.logo{
 display:flex;align-items:center;gap:10px;font-size:24px;
 font-weight:800;color:var(--primary)
}

.logo-icon{
 width:40px;height:40px;border-radius:12px;
 background:linear-gradient(135deg,#2563eb,#06b6d4);
 display:grid;place-items:center;color:#fff;transform:rotate(-10deg)
}

.nav-links{display:flex;gap:30px;align-items:center}
.nav-links a{text-decoration:none;color:var(--text);font-size:14px;font-weight:600}
.nav-links a:hover{color:var(--primary)}

.login-btn{
 border:1px solid var(--border);padding:10px 18px;border-radius:12px;
 background:#fff;cursor:pointer;font-weight:600
}

.hero{
 min-height:500px;
 background:
 linear-gradient(120deg,rgba(15,23,42,.86),rgba(37,99,235,.62)),
 url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1800&q=85")
 center/cover;
 padding:75px 6% 120px;color:#fff
}

.hero-content{max-width:1200px;margin:auto}
.hero h1{
 font-size:clamp(38px,5vw,64px);line-height:1.05;
 max-width:750px;letter-spacing:-2px
}
.hero p{margin-top:18px;color:#dbeafe;font-size:18px}

.booking-box{
 max-width:1200px;margin:-85px auto 0;position:relative;z-index:5;
 background:rgba(255,255,255,.96);backdrop-filter:blur(20px);
 border-radius:24px;padding:28px;
 box-shadow:0 25px 70px rgba(15,23,42,.18)
}

.trip-tabs{display:flex;gap:8px;margin-bottom:25px}
.trip-tab{
 padding:10px 18px;border:0;border-radius:10px;background:transparent;
 cursor:pointer;font-weight:600;color:var(--muted)
}
.trip-tab.active{background:#dbeafe;color:var(--primary)}

.search-grid{
 display:grid;
 grid-template-columns:1.2fr 1.2fr 1fr 1fr 1.2fr auto;
 gap:12px;align-items:end
}

.field{position:relative}
.field label{
 display:block;font-size:12px;color:var(--muted);font-weight:700;
 margin-bottom:7px;text-transform:uppercase;letter-spacing:.5px
}

.field input,.field select{
 width:100%;height:54px;border:1px solid var(--border);
 border-radius:14px;padding:0 15px;outline:none;background:#fff;
 font-size:14px;color:var(--dark)
}

.field input:focus,.field select:focus{
 border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,.1)
}

.location-input{padding-left:42px!important}
.location-icon{
 position:absolute;left:14px;bottom:17px;color:var(--primary)
}

.swap-btn{
 width:40px;height:40px;border-radius:50%;border:1px solid var(--border);
 background:#fff;color:var(--primary);cursor:pointer;
 position:absolute;right:-26px;bottom:7px;z-index:2;
 box-shadow:0 5px 15px rgba(0,0,0,.08)
}
.swap-btn:hover{transform:rotate(180deg);transition:.3s}

.search-btn{
 height:54px;border:0;border-radius:14px;padding:0 25px;
 background:linear-gradient(135deg,var(--primary),var(--accent));
 color:#fff;font-weight:800;cursor:pointer;
 box-shadow:0 10px 25px rgba(37,99,235,.25)
}
.search-btn:hover{transform:translateY(-2px)}

.main{max-width:1200px;margin:55px auto;padding:0 20px}
.section-heading{
 display:flex;justify-content:space-between;align-items:center;margin-bottom:22px
}
.section-heading h2{font-size:28px}
.section-heading p{color:var(--muted);margin-top:5px}

.quick-grid{
 display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-bottom:60px
}

.quick-card{
 background:#fff;border:1px solid var(--border);border-radius:18px;
 padding:22px;transition:.25s
}
.quick-card:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
.quick-icon{
 width:45px;height:45px;border-radius:13px;background:#eff6ff;
 display:grid;place-items:center;font-size:21px;margin-bottom:14px
}
.quick-card h3{font-size:16px;margin-bottom:6px}
.quick-card p{color:var(--muted);font-size:13px}

.results-layout{
 display:grid;grid-template-columns:230px 1fr;gap:25px
}

.filters{
 background:#fff;border-radius:18px;border:1px solid var(--border);
 padding:20px;height:fit-content
}
.filters h3{margin-bottom:20px}
.filter-group{margin-bottom:25px}
.filter-group h4{font-size:13px;margin-bottom:12px}
.filter-option{
 display:flex;gap:9px;align-items:center;margin:10px 0;
 font-size:13px;color:var(--text)
}

.flight-list{display:flex;flex-direction:column;gap:15px}
.flight-card{
 background:#fff;border:1px solid var(--border);border-radius:20px;
 padding:22px;transition:.2s
}
.flight-card:hover{border-color:#bfdbfe;box-shadow:var(--shadow)}

.flight-top{display:flex;justify-content:space-between;margin-bottom:20px}
.airline{display:flex;align-items:center;gap:12px}
.airline-logo{
 width:42px;height:42px;border-radius:12px;background:#eff6ff;
 display:grid;place-items:center;font-size:20px
}
.airline strong{display:block}
.airline span{font-size:12px;color:var(--muted)}

.price{text-align:right}
.price strong{font-size:22px}
.price span{font-size:11px;color:var(--muted)}

.flight-route{
 display:grid;grid-template-columns:1fr 100px 1fr;
 align-items:center;gap:15px
}
.airport h3{font-size:24px}
.airport p{font-size:12px;color:var(--muted)}
.airport.right{text-align:right}

.route-line{text-align:center;position:relative}
.route-line span{
 display:block;font-size:11px;color:var(--muted);margin-bottom:8px
}
.line{height:1px;background:#cbd5e1;position:relative}
.plane{
 position:absolute;left:50%;top:-10px;transform:translateX(-50%);
 background:#fff;padding:0 5px;color:var(--primary)
}

.flight-bottom{
 display:flex;justify-content:space-between;align-items:center;
 margin-top:20px;padding-top:15px;border-top:1px solid #f1f5f9
}
.tags{display:flex;gap:8px;flex-wrap:wrap}
.tag{
 padding:6px 9px;background:#f0fdf4;color:var(--success);
 border-radius:8px;font-size:11px;font-weight:700
}
.select-btn{
 background:var(--dark);color:#fff;border:0;border-radius:10px;
 padding:11px 20px;cursor:pointer;font-weight:700
}
.select-btn:hover{background:var(--primary)}

.empty-state{
 background:#fff;border:1px dashed #cbd5e1;border-radius:18px;
 padding:45px;text-align:center;color:var(--muted)
}

.modal{
 position:fixed;inset:0;background:rgba(15,23,42,.6);
 backdrop-filter:blur(5px);display:none;align-items:center;
 justify-content:center;z-index:999;padding:20px
}
.modal.active{display:flex}
.modal-box{
 background:#fff;width:100%;max-width:500px;border-radius:24px;
 padding:30px;animation:pop .25s ease
}
@keyframes pop{
 from{transform:scale(.95);opacity:0}
 to{transform:scale(1);opacity:1}
}
.modal-header{display:flex;justify-content:space-between;margin-bottom:25px}
.close{
 border:0;background:#f1f5f9;width:35px;height:35px;
 border-radius:50%;cursor:pointer
}
.booking-summary{
 background:#f8fafc;padding:18px;border-radius:15px;margin-bottom:20px
}
.confirm-btn{
 width:100%;height:50px;border:0;border-radius:12px;
 background:var(--primary);color:#fff;font-weight:800;cursor:pointer
}

.toast{
 position:fixed;right:25px;bottom:25px;background:#0f172a;color:#fff;
 padding:15px 20px;border-radius:13px;box-shadow:var(--shadow);
 transform:translateY(120px);opacity:0;transition:.3s;z-index:1000
}
.toast.show{transform:translateY(0);opacity:1}

@media(max-width:1000px){
 .search-grid{grid-template-columns:repeat(2,1fr)}
 .search-btn{width:100%}
 .quick-grid{grid-template-columns:repeat(2,1fr)}
 .results-layout{grid-template-columns:1fr}
 .filters{display:none}
}

@media(max-width:650px){
 .navbar{padding:0 20px}
 .nav-links{display:none}
 .hero{padding:55px 20px 110px}
 .booking-box{margin:-70px 15px 0;padding:20px}
 .search-grid{grid-template-columns:1fr}
 .quick-grid{grid-template-columns:1fr}
 .flight-route{grid-template-columns:1fr}
 .airport.right{text-align:left}
 .route-line{margin:5px 0}
 .flight-bottom{flex-direction:column;align-items:flex-start;gap:15px}
 .select-btn{width:100%}
}
</style>
</head>

<body>

<nav class="navbar">
 <div class="logo">
  <div class="logo-icon">✈</div>
  SkyBook
 </div>
 <div class="nav-links">
  <a href="#results">Flights</a>
  <a href="#">Hotels</a>
  <a href="#">Trips</a>
  <a href="#">Deals</a>
  <button class="login-btn" onclick="showToast('Sign-in is ready for backend integration.')">Sign in</button>
 </div>
</nav>

<section class="hero">
 <div class="hero-content">
  <h1>Fly somewhere<br>you'll love.</h1>
  <p>Search hundreds of flights and find the perfect journey for your next adventure.</p>
 </div>
</section>

<section class="booking-box">
 <div class="trip-tabs">
  <button class="trip-tab active" onclick="setTrip(this,'round')">Round trip</button>
  <button class="trip-tab" onclick="setTrip(this,'oneway')">One way</button>
  <button class="trip-tab" onclick="setTrip(this,'multi')">Multi-city</button>
 </div>

 <div class="search-grid">
  <div class="field">
   <label>From</label>
   <span class="location-icon">📍</span>
   <input id="from" class="location-input" value="Hyderabad (HYD)">
  </div>

  <div class="field">
   <label>To</label>
   <span class="location-icon">📍</span>
   <input id="to" class="location-input" value="Delhi (DEL)">
   <button class="swap-btn" onclick="swapCities()" title="Swap cities">⇄</button>
  </div>

  <div class="field">
   <label>Departure</label>
   <input id="departure" type="date">
  </div>

  <div class="field" id="returnField">
   <label>Return</label>
   <input id="returnDate" type="date">
  </div>

  <div class="field">
   <label>Passengers</label>
   <select id="passengers">
    <option value="1">1 Passenger · Economy</option>
    <option value="2">2 Passengers · Economy</option>
    <option value="3">3 Passengers · Economy</option>
    <option value="4">4 Passengers · Economy</option>
    <option value="1-business">1 Passenger · Business</option>
   </select>
  </div>

  <button class="search-btn" onclick="searchFlights()">Search ✦</button>
 </div>
</section>

<main class="main">

 <section>
  <div class="section-heading">
   <div>
    <h2>Travel made simple</h2>
    <p>Everything you need for your next journey.</p>
   </div>
  </div>

  <div class="quick-grid">
   <div class="quick-card">
    <div class="quick-icon">🔎</div>
    <h3>Compare flights</h3>
    <p>Compare prices and schedules from multiple airlines.</p>
   </div>
   <div class="quick-card">
    <div class="quick-icon">⚡</div>
    <h3>Fast booking</h3>
    <p>Book your flight in just a few simple steps.</p>
   </div>
   <div class="quick-card">
    <div class="quick-icon">💳</div>
    <h3>Secure payments</h3>
    <p>Your booking and payment information stays protected.</p>
   </div>
   <div class="quick-card">
    <div class="quick-icon">🎧</div>
    <h3>24/7 support</h3>
    <p>Get help whenever you need it during your journey.</p>
   </div>
  </div>
 </section>

 <section id="results">
  <div class="section-heading">
   <div>
    <h2>Available flights</h2>
    <p id="resultText">Best options for your journey</p>
   </div>
  </div>

  <div class="results-layout">

   <aside class="filters">
    <h3>Filters</h3>

    <div class="filter-group">
     <h4>Stops</h4>
     <label class="filter-option">
      <input type="checkbox" class="stop-filter" value="Non-stop" checked>
      Non-stop
     </label>
     <label class="filter-option">
      <input type="checkbox" class="stop-filter" value="1 Stop">
      1 Stop
     </label>
    </div>

    <div class="filter-group">
     <h4>Airlines</h4>
     <label class="filter-option">
      <input type="checkbox" class="airline-filter" value="IndiGo" checked>
      IndiGo
     </label>
     <label class="filter-option">
      <input type="checkbox" class="airline-filter" value="Air India" checked>
      Air India
     </label>
     <label class="filter-option">
      <input type="checkbox" class="airline-filter" value="Vistara" checked>
      Vistara
     </label>
    </div>

    <div class="filter-group">
     <h4>Departure time</h4>
     <label class="filter-option">
      <input type="checkbox" class="time-filter" value="Morning">
      Morning
     </label>
     <label class="filter-option">
      <input type="checkbox" class="time-filter" value="Afternoon">
      Afternoon
     </label>
     <label class="filter-option">
      <input type="checkbox" class="time-filter" value="Evening">
      Evening
     </label>
    </div>

    <div class="filter-group">
     <h4>Maximum price</h4>
     <input id="priceFilter" type="range" min="3000" max="10000" value="10000"
            style="width:100%" oninput="updatePriceLabel()">
     <div style="font-size:12px;color:#64748b;margin-top:7px">
      Up to <strong id="priceLabel">₹10,000</strong>
     </div>
    </div>
   </aside>

   <div class="flight-list" id="flightList"></div>

  </div>
 </section>
</main>

<div class="modal" id="bookingModal">
 <div class="modal-box">
  <div class="modal-header">
   <div>
    <h2>Confirm your flight</h2>
    <p style="color:#64748b;margin-top:5px;">Review your selection</p>
   </div>
   <button class="close" onclick="closeModal()">✕</button>
  </div>
  <div class="booking-summary" id="bookingSummary"></div>
  <button class="confirm-btn" onclick="confirmBooking()">
   Continue to Passenger Details →
  </button>
 </div>
</div>

<div class="toast" id="toast"></div>

<script>
const flights = {{ flights|tojson }};

let currentTrip = "round";

function formatPrice(value) {
 return "₹" + Number(value).toLocaleString("en-IN");
}

function getTimeCategory(time) {
 const hour = Number(time.split(":")[0]);
 if (hour < 12) return "Morning";
 if (hour < 17) return "Afternoon";
 return "Evening";
}

function displayFlights(data = flights) {
 const list = document.getElementById("flightList");

 if (!data.length) {
  list.innerHTML = `
   <div class="empty-state">
    <div style="font-size:35px;margin-bottom:12px">🛫</div>
    <h3>No flights found</h3>
    <p style="margin-top:8px">Try changing your filters or search criteria.</p>
   </div>`;
  return;
 }

 list.innerHTML = data.map(flight => `
  <div class="flight-card">
   <div class="flight-top">
    <div class="airline">
     <div class="airline-logo">${flight.logo}</div>
     <div>
      <strong>${flight.airline}</strong>
      <span>${flight.number} · Economy</span>
     </div>
    </div>
    <div class="price">
     <strong>${formatPrice(flight.price)}</strong>
     <span>per passenger</span>
    </div>
   </div>

   <div class="flight-route">
    <div class="airport">
     <h3>${flight.departure}</h3>
     <strong>${flight.from}</strong>
     <p>${flight.from_city}</p>
    </div>

    <div class="route-line">
     <span>${flight.duration}</span>
     <div class="line"><div class="plane">✈</div></div>
     <small style="color:#16a34a;font-size:10px">${flight.tag}</small>
    </div>

    <div class="airport right">
     <h3>${flight.arrival}</h3>
     <strong>${flight.to}</strong>
     <p>${flight.to_city}</p>
    </div>
   </div>

   <div class="flight-bottom">
    <div class="tags">
     <span class="tag">✓ ${flight.tag}</span>
     <span class="tag">✓ Cabin bag</span>
    </div>
    <button class="select-btn" onclick="selectFlight(${flight.id})">
     Select flight
    </button>
   </div>
  </div>
 `).join("");
}

function swapCities() {
 const from = document.getElementById("from");
 const to = document.getElementById("to");
 [from.value, to.value] = [to.value, from.value];
 showToast("Departure and destination swapped.");
}

function setTrip(button, type) {
 document.querySelectorAll(".trip-tab").forEach(tab =>
  tab.classList.remove("active")
 );
 button.classList.add("active");
 currentTrip = type;

 const returnField = document.getElementById("returnField");
 const returnDate = document.getElementById("returnDate");

 if (type === "oneway") {
  returnField.style.opacity = ".4";
  returnDate.disabled = true;
 } else {
  returnField.style.opacity = "1";
  returnDate.disabled = false;
 }

 if (type === "multi") {
  showToast("Multi-city mode selected. Additional legs can be added in the backend.");
 }
}

function searchFlights() {
 const from = document.getElementById("from").value.trim();
 const to = document.getElementById("to").value.trim();
 const date = document.getElementById("departure").value;

 if (!from || !to) {
  showToast("Please enter departure and destination.");
  return;
 }

 document.getElementById("resultText").innerText =
  `Flights from ${from} to ${to}${date ? " · " + date : ""}`;

 document.getElementById("results").scrollIntoView({behavior:"smooth"});
 displayFlights();

 showToast("Flight search completed.");
}

function selectFlight(id) {
 const flight = flights.find(item => item.id === id);
 if (!flight) return;

 const passengerValue = document.getElementById("passengers").value;
 const passengerCount = passengerValue.split("-")[0];
 const total = flight.price * Number(passengerCount);

 document.getElementById("bookingSummary").innerHTML = `
  <strong>${flight.airline} · ${flight.number}</strong>

  <div style="display:flex;justify-content:space-between;
              margin-top:15px;gap:15px">
   <div>
    <strong style="font-size:20px">${flight.departure}</strong>
    <p>${flight.from}</p>
   </div>

   <div style="color:#64748b;text-align:center">
    ${flight.duration}<br>✈
   </div>

   <div style="text-align:right">
    <strong style="font-size:20px">${flight.arrival}</strong>
    <p>${flight.to}</p>
   </div>
  </div>

  <hr style="border:0;border-top:1px solid #e2e8f0;margin:15px 0">

  <div style="display:flex;justify-content:space-between">
   <span>Passengers</span>
   <strong>${passengerCount}</strong>
  </div>

  <div style="display:flex;justify-content:space-between;margin-top:8px">
   <span>Total fare</span>
   <strong>${formatPrice(total)}</strong>
  </div>
 `;

 document.getElementById("bookingModal").classList.add("active");
}

function closeModal() {
 document.getElementById("bookingModal").classList.remove("active");
}

function confirmBooking() {
 closeModal();
 showToast("Flight selected! Passenger details can be added next.");
}

function updatePriceLabel() {
 const value = document.getElementById("priceFilter").value;
 document.getElementById("priceLabel").innerText = formatPrice(value);
 applyFilters();
}

function applyFilters() {
 const airlines = [...document.querySelectorAll(".airline-filter:checked")]
  .map(item => item.value);

 const times = [...document.querySelectorAll(".time-filter:checked")]
  .map(item => item.value);

 const maxPrice = Number(document.getElementById("priceFilter").value);

 const filtered = flights.filter(flight => {
  const airlineMatch = airlines.length === 0 || airlines.includes(flight.airline);
  const timeMatch = times.length === 0 ||
                    times.includes(getTimeCategory(flight.departure));
  const priceMatch = flight.price <= maxPrice;
  return airlineMatch && timeMatch && priceMatch;
 });

 displayFlights(filtered);
}

function showToast(message) {
 const toast = document.getElementById("toast");
 toast.innerText = message;
 toast.classList.add("show");

 clearTimeout(window.toastTimer);
 window.toastTimer = setTimeout(() => {
  toast.classList.remove("show");
 }, 2800);
}

document.querySelectorAll(
 ".airline-filter,.stop-filter,.time-filter"
).forEach(input => input.addEventListener("change", applyFilters));

const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(today.getDate() + 1);

const nextWeek = new Date(today);
nextWeek.setDate(today.getDate() + 8);

document.getElementById("departure").value =
 tomorrow.toISOString().split("T")[0];

document.getElementById("returnDate").value =
 nextWeek.toISOString().split("T")[0];

displayFlights();

document.getElementById("bookingModal").addEventListener("click", event => {
 if (event.target.id === "bookingModal") closeModal();
});
</script>

</body>
</html>
"""

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/")
def home():
    return render_template_string(PAGE, flights=FLIGHTS)


@app.route("/api/flights")
def api_flights():
    return jsonify(FLIGHTS)


@app.route("/api/search")
def search():
    from_city = request.args.get("from", "").strip().lower()
    to_city = request.args.get("to", "").strip().lower()

    results = FLIGHTS

    if from_city:
        results = [
            flight for flight in results
            if from_city in flight["from_city"].lower()
            or from_city in flight["from"].lower()
        ]

    if to_city:
        results = [
            flight for flight in results
            if to_city in flight["to_city"].lower()
            or to_city in flight["to"].lower()
        ]

    return jsonify(results)


@app.route("/api/book", methods=["POST"])
def book():
    data = request.get_json(silent=True) or {}
    flight_id = data.get("flight_id")
    passengers = data.get("passengers", 1)

    flight = next(
        (item for item in FLIGHTS if item["id"] == flight_id),
        None
    )

    if not flight:
        return jsonify({
            "success": False,
            "message": "Flight not found."
        }), 404

    try:
        passengers = int(passengers)
        if passengers < 1:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Invalid passenger count."
        }), 400

    return jsonify({
        "success": True,
        "message": "Flight selected successfully.",
        "booking": {
            "flight_number": flight["number"],
            "airline": flight["airline"],
            "passengers": passengers,
            "total": flight["price"] * passengers
        }
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
