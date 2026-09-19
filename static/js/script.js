//const api = (url, options={}) => fetch(url, {credentials: "same-origin", headers: {"Content-Type":"application/json", "X-CSRFToken": getCookie("csrftoken"), ...(options.headers||{})}, ...options});
//function getCookie(name) { return document.cookie.split("; ").find(x=>x.startsWith(name+"="))?.split("=")[1] || ""; }
//function escapeHtml(text) { const e=document.createElement("span"); e.textContent=text; return e.innerHTML; }
//async function json(url, options) { const r=await api(url,options); if(r.status===403){ location.href="/login/"; throw Error("Please log in"); } const d=await r.json(); if(!r.ok) throw Error(typeof d==="string" ? d : JSON.stringify(d)); return d; }
//async function loadDashboard(){
// const [summary,records,donations,me]=await Promise.all([json("/api/analytics/summary/"),json("/api/food/waste/"),json("/api/donations/"),json("/api/users/me/")]);
// document.querySelector("#welcome").textContent=`Hello, ${me.username} (${me.role})`;
// document.querySelector("#prepared").textContent=summary.total_prepared+" kg"; document.querySelector("#wasted").textContent=summary.total_wasted+" kg"; document.querySelector("#percentage").textContent=summary.waste_percentage+"%";
// document.querySelector("#donations").textContent=donations.filter(x=>x.status==="AVAILABLE").length;
// document.querySelector("#recent").innerHTML=records.slice(0,5).map(x=>`<tr><td>${x.date}</td><td>${escapeHtml(x.source)}</td><td>${escapeHtml(x.food_type)}</td><td>${x.prepared_quantity} kg</td><td>${x.wasted_quantity} kg</td></tr>`).join("") || "<tr><td colspan='5'>No records yet.</td></tr>";
//}
//async function loadFood(){ const list=await json("/api/food/waste/"); document.querySelector("#waste-list").innerHTML=list.map(x=>`<tr><td>${x.date}</td><td>${escapeHtml(x.source)}</td><td>${escapeHtml(x.food_type)}</td><td>${x.prepared_quantity}</td><td>${x.wasted_quantity}</td><td><button onclick="deleteRecord(${x.id})">Delete</button></td></tr>`).join("") || "<tr><td colspan='6'>No records yet.</td></tr>"; }
//async function deleteRecord(id){ if(confirm("Delete this record?")){ await json(`/api/food/waste/${id}/`,{method:"DELETE"}); loadFood(); } }
//async function loadAnalytics(){ const s=await json("/api/analytics/summary/"); document.querySelector("#average").textContent=s.average_waste+" kg"; document.querySelector("#maximum").textContent=s.maximum_waste+" kg"; document.querySelector("#minimum").textContent=s.minimum_waste+" kg"; document.querySelector("#most-wasted").textContent=s.most_wasted_food_type; }
//document.addEventListener("DOMContentLoaded",()=>{
// const p=location.pathname;
// if(p==="/") loadDashboard().catch(console.error); if(p==="/food/") { loadFood().catch(console.error); document.querySelector("#waste-form").onsubmit=async e=>{e.preventDefault(); const d=Object.fromEntries(new FormData(e.target)); try { await json("/api/food/waste/",{method:"POST",body:JSON.stringify(d)}); e.target.reset(); document.querySelector("#form-message").textContent="Record saved."; loadFood(); } catch(err){document.querySelector("#form-message").textContent=err.message;} }; }
// if(p==="/analytics/"){ loadAnalytics().catch(console.error); document.querySelector("#generate-charts").onclick=async()=>{const c=await json("/api/analytics/charts/",{method:"POST",body:"{}"}); document.querySelector("#chart-box").innerHTML=`<img src="${c.food_type_chart}?${Date.now()}"><img src="${c.trend_chart}?${Date.now()}">`;}; }
// if(p==="/login/") document.querySelector("#login-form").onsubmit=async e=>{e.preventDefault(); try {await json("/api/users/login/",{method:"POST",body:JSON.stringify(Object.fromEntries(new FormData(e.target)))});location.href="/";}catch(err){document.querySelector("#auth-message").textContent=err.message;}};
// if(p==="/register/") document.querySelector("#register-form").onsubmit=async e=>{e.preventDefault(); try {await json("/api/users/register/",{method:"POST",body:JSON.stringify(Object.fromEntries(new FormData(e.target)))});location.href="/login/";}catch(err){document.querySelector("#auth-message").textContent=err.message;}};
// document.querySelector("#logout")?.addEventListener("click",async()=>{await json("/api/users/logout/",{method:"POST",body:"{}"});location.href="/login/";});
//});



function getCookie(name) {
    return document.cookie
        .split("; ")
        .find(x => x.startsWith(name + "="))
        ?.split("=")[1] || "";
}


const api = (url, options = {}) => {

    return fetch(url, {
        credentials: "same-origin",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
            ...(options.headers || {})
        },

        ...options
    });

};


function escapeHtml(text) {

    const element = document.createElement("span");

    element.textContent = text ?? "";

    return element.innerHTML;

}


async function json(url, options = {}) {

    const response = await api(url, options);

    if (response.status === 403) {

        location.href = "/login/";

        throw new Error("Please log in");

    }

    let data;

    try {

        data = await response.json();

    } catch {

        throw new Error("Invalid server response");

    }

    if (!response.ok) {

        throw new Error(
            typeof data === "string"
                ? data
                : JSON.stringify(data)
        );

    }

    return data;

}


/* =========================
   DASHBOARD
========================= */

async function loadDashboard() {

    try {

        const [summary, records, donations, me] = await Promise.all([

            json("/api/analytics/summary/"),

            json("/api/food/waste/"),

            json("/api/donations/"),

            json("/api/users/me/")

        ]);


        /* Welcome message */

        const welcome = document.querySelector("#welcome");

        if (welcome) {

            welcome.textContent =
                `Hello, ${me.username} (${me.role})`;

        }


        /* Summary */

        const prepared = document.querySelector("#prepared");

        if (prepared) {

            prepared.textContent =
                (summary.total_prepared ?? 0) + " kg";

        }


        const wasted = document.querySelector("#wasted");

        if (wasted) {

            wasted.textContent =
                (summary.total_wasted ?? 0) + " kg";

        }


        const percentage = document.querySelector("#percentage");

        if (percentage) {

            percentage.textContent =
                (summary.waste_percentage ?? 0) + "%";

        }


        /* Donations */

        const donationCount =
            document.querySelector("#donations");

        if (donationCount) {

            const donationList =
                Array.isArray(donations)
                    ? donations
                    : donations.results || [];

            donationCount.textContent =
                donationList.filter(
                    x => x.status === "AVAILABLE"
                ).length;

        }


        /* Food records */

        const recent =
            document.querySelector("#recent");

        if (recent) {

            const foodRecords =
                Array.isArray(records)
                    ? records
                    : records.results || [];


            recent.innerHTML =
                foodRecords
                    .slice(0, 5)
                    .map(x => `

                        <tr>

                            <td>
                                ${x.date ?? ""}
                            </td>

                            <td>
                                ${escapeHtml(x.source)}
                            </td>

                            <td>
                                ${escapeHtml(x.food_type)}
                            </td>

                            <td>
                                ${x.prepared_quantity ?? 0} kg
                            </td>

                            <td>
                                ${x.wasted_quantity ?? 0} kg
                            </td>

                        </tr>

                    `)
                    .join("");


            if (!recent.innerHTML) {

                recent.innerHTML =
                    "<tr><td colspan='5'>No records yet.</td></tr>";

            }

        }

    } catch (error) {

        console.error("Dashboard error:", error);

    }

}


/* =========================
   FOOD WASTE
========================= */

async function loadFood() {

    try {

        const data =
            await json("/api/food/waste/");


        const records =
            Array.isArray(data)
                ? data
                : data.results || [];


        const list =
            document.querySelector("#waste-list");


        if (!list) {

            return;

        }


        list.innerHTML =
            records
                .map(x => `

                    <tr>

                        <td>
                            ${x.date ?? ""}
                        </td>

                        <td>
                            ${escapeHtml(x.source)}
                        </td>

                        <td>
                            ${escapeHtml(x.food_type)}
                        </td>

                        <td>
                            ${x.prepared_quantity ?? 0}
                        </td>

                        <td>
                            ${x.wasted_quantity ?? 0}
                        </td>

                        <td>

                            <button
                                onclick="deleteRecord(${x.id})"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>

                `)
                .join("");


        if (!list.innerHTML) {

            list.innerHTML =
                "<tr><td colspan='6'>No records yet.</td></tr>";

        }

    } catch (error) {

        console.error("Food loading error:", error);

    }

}


/* =========================
   DELETE FOOD RECORD
========================= */

async function deleteRecord(id) {

    if (!confirm("Delete this record?")) {

        return;

    }


    try {

        await json(
            `/api/food/waste/${id}/`,
            {
                method: "DELETE"
            }
        );


        loadFood();


    } catch (error) {

        console.error("Delete error:", error);

        alert(error.message);

    }

}


/* =========================
   ADD FOOD WASTE
========================= */

async function addFoodWaste(event) {

    event.preventDefault();


    const form = event.target;

    const formMessage =
        document.querySelector("#form-message");


    const data =
        Object.fromEntries(
            new FormData(form)
        );


    try {

        await json(
            "/api/food/waste/",
            {
                method: "POST",

                body: JSON.stringify(data)
            }
        );


        form.reset();


        if (formMessage) {

            formMessage.textContent =
                "Record saved successfully.";

        }


        loadFood();


    } catch (error) {

        console.error("Save error:", error);


        if (formMessage) {

            formMessage.textContent =
                error.message;

        }

    }

}


/* =========================
   ANALYTICS
========================= */

async function loadAnalytics() {

    try {

        const summary =
            await json(
                "/api/analytics/summary/"
            );


        const average =
            document.querySelector("#average");

        if (average) {

            average.textContent =
                (summary.average_waste ?? 0) + " kg";

        }


        const maximum =
            document.querySelector("#maximum");

        if (maximum) {

            maximum.textContent =
                (summary.maximum_waste ?? 0) + " kg";

        }


        const minimum =
            document.querySelector("#minimum");

        if (minimum) {

            minimum.textContent =
                (summary.minimum_waste ?? 0) + " kg";

        }


        const mostWasted =
            document.querySelector("#most-wasted");

        if (mostWasted) {

            mostWasted.textContent =
                summary.most_wasted_food_type || "No data";

        }

    } catch (error) {

        console.error(
            "Analytics error:",
            error
        );

    }

}


/* =========================
   GENERATE CHARTS
========================= */

async function generateCharts() {

    try {

        const chartData =
            await json(
                "/api/analytics/charts/",
                {
                    method: "POST",
                    body: "{}"
                }
            );


        const chartBox =
            document.querySelector("#chart-box");


        if (!chartBox) {

            return;

        }


        chartBox.innerHTML = `

            <img
                src="${chartData.food_type_chart}?${Date.now()}"
                alt="Food Type Waste Chart"
            >

            <img
                src="${chartData.trend_chart}?${Date.now()}"
                alt="Food Waste Trend Chart"
            >

        `;

    } catch (error) {

        console.error(
            "Chart generation error:",
            error
        );

    }

}


/* =========================
   LOGIN
========================= */

async function loginUser(event) {

    event.preventDefault();


    const form = event.target;


    const data =
        Object.fromEntries(
            new FormData(form)
        );


    try {

        await json(
            "/api/users/login/",
            {
                method: "POST",

                body: JSON.stringify(data)
            }
        );


        location.href = "/";


    } catch (error) {

        const message =
            document.querySelector("#auth-message");


        if (message) {

            message.textContent =
                error.message;

        }

    }

}


/* =========================
   REGISTER
========================= */

async function registerUser(event) {

    event.preventDefault();


    const form = event.target;


    const data =
        Object.fromEntries(
            new FormData(form)
        );


    try {

        await json(
            "/api/users/register/",
            {
                method: "POST",

                body: JSON.stringify(data)
            }
        );


        location.href = "/login/";


    } catch (error) {

        const message =
            document.querySelector("#auth-message");


        if (message) {

            message.textContent =
                error.message;

        }

    }

}


/* =========================
   LOGOUT
========================= */

async function logoutUser() {

    try {

        await json(
            "/api/users/logout/",
            {
                method: "POST",

                body: "{}"
            }
        );


        location.href = "/login/";


    } catch (error) {

        console.error(
            "Logout error:",
            error
        );

    }

}


/* =========================
   PAGE LOAD
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const path =
            location.pathname;


        /* Dashboard */

        if (path === "/") {

            loadDashboard();

        }


        /* Food page */

        if (path === "/food/") {

            loadFood();


            const wasteForm =
                document.querySelector(
                    "#waste-form"
                );


            if (wasteForm) {

                wasteForm.addEventListener(
                    "submit",
                    addFoodWaste
                );

            }

        }


        /* Analytics page */

        if (path === "/analytics/") {

            loadAnalytics();


            const chartButton =
                document.querySelector(
                    "#generate-charts"
                );


            if (chartButton) {

                chartButton.addEventListener(
                    "click",
                    generateCharts
                );

            }

        }


        /* Login page */

        if (path === "/login/") {

            const loginForm =
                document.querySelector(
                    "#login-form"
                );


            if (loginForm) {

                loginForm.addEventListener(
                    "submit",
                    loginUser
                );

            }

        }


        /* Register page */

        if (path === "/register/") {

            const registerForm =
                document.querySelector(
                    "#register-form"
                );


            if (registerForm) {

                registerForm.addEventListener(
                    "submit",
                    registerUser
                );

            }

        }


        /* Logout */

        const logoutButton =
            document.querySelector(
                "#logout"
            );


        if (logoutButton) {

            logoutButton.addEventListener(
                "click",
                logoutUser
            );

        }

    }
);
/* Role-specific dashboards */
function recordsOf(data) { return Array.isArray(data) ? data : (data.results || []); }
async function createDonation(event) {
    event.preventDefault();
    const message = document.querySelector("#donation-message");
    try {
        const data = Object.fromEntries(new FormData(event.target));
        data.available_until = new Date(data.available_until).toISOString();
        await json("/api/donations/", {method: "POST", body: JSON.stringify(data)});
        event.target.reset(); message.textContent = "Donation listed as available.";
        loadDashboard();
    } catch (error) { message.textContent = error.message; }
}
async function claimDonation(id) {
    try { await json(`/api/donations/${id}/claim/`, {method:"POST", body:"{}"}); loadNgoDashboard(); }
    catch (error) { alert(error.message); }
}
async function collectDonation(id) {
    try { await json(`/api/donations/${id}/collect/`, {method:"POST", body:"{}"}); loadNgoDashboard(); }
    catch (error) { alert(error.message); }
}
async function loadNgoDashboard() {
    const [data, me] = await Promise.all([json("/api/donations/"), json("/api/users/me/")]);
    const donations = recordsOf(data);
    const available = donations.filter(x => x.status === "AVAILABLE");
    const mine = donations.filter(x => x.collection_volunteer === me.username);
    document.querySelector("#available-count").textContent = available.length;
    document.querySelector("#claimed-count").textContent = mine.filter(x => x.status === "CLAIMED").length;
    document.querySelector("#collected-count").textContent = mine.filter(x => x.status === "COLLECTED").length;
    document.querySelector("#donation-list").innerHTML = donations.map(x => {
        let action = "—";
        if (x.status === "AVAILABLE") action = `<button onclick="claimDonation(${x.id})">Claim</button>`;
        if (x.status === "CLAIMED" && x.collection_volunteer === me.username) action = `<button onclick="collectDonation(${x.id})">Mark collected</button>`;
        return `<tr><td>${escapeHtml(x.food_name)}</td><td>${x.quantity} kg</td><td>${escapeHtml(x.provider_name)}</td><td>${escapeHtml(x.pickup_address)}</td><td>${new Date(x.available_until).toLocaleString()}</td><td>${x.status}</td><td>${action}</td></tr>`;
    }).join("") || "<tr><td colspan='7'>No donations available.</td></tr>";
}
async function loadAdminDonations() {
    const donations = recordsOf(await json("/api/donations/"));
    const target = document.querySelector("#admin-donations");
    if (target) target.innerHTML = donations.map(x => `<tr><td>${escapeHtml(x.food_name)}</td><td>${x.quantity} kg</td><td>${escapeHtml(x.provider_name)}</td><td>${x.status}</td></tr>`).join("") || "<tr><td colspan='4'>No donations yet.</td></tr>";
}
const existingLoad = loadDashboard;
loadDashboard = async function () { await existingLoad(); if (location.pathname === "/dashboard/admin/") await loadAdminDonations(); };
document.addEventListener("DOMContentLoaded", () => {
    if (location.pathname === "/dashboard/provider/") document.querySelector("#donation-form")?.addEventListener("submit", createDonation);
    if (location.pathname === "/dashboard/ngo/") loadNgoDashboard().catch(console.error);
});

document.addEventListener("DOMContentLoaded", () => {
    if (["/dashboard/provider/", "/dashboard/admin/"].includes(location.pathname)) {
        loadDashboard().catch(console.error);
    }
});
