function req(url, options) {
    window.fetch(url, options)
    .then(res => {
        if(!res.ok) {
            let msg = ""+
            `Erro ${res.status}: ${res.statusText}\n`+
            "Try again! If the problem persists, contact the support!";

            alert(msg);
        } else {
            window.open(res.url, "_self");
        }
    })
    .catch(err => {
        const msg = ""+
        "Something went wrong.\n"+
        "Try again! If the problem persists, contact the support!";
        
        console.log(err);
        alert(msg);
    });
}

function setTimezoneInfo(dt_iso) {
    const dt = new Date(dt_iso);
    const dt_utc = dt.toISOString();

    return dt_utc;
}

function getData(form) {
    const data = {};
    data.task_id = form.task_id.value;
    data.title = form.title.value;
    data.description = form.description.value;
    data.start_time = setTimezoneInfo(form.start_time.value);
    data.end_time = setTimezoneInfo(form.end_time.value);
    data.priority = form.priority.value;
    data.status = form.status.value;

    return data;
}

function onSearch(event) {
    event.preventDefault();
    const form = event.target;
    const url = form.action + "?search=" + form.search.value;
    const options = {method: "GET"};

    req(url, options);
}

function onCreateOrUpdate(event) {
    event.preventDefault();
    const form = event.target;
    const url = form.action;
    const data = getData(form);
    const dataJSON = JSON.stringify(data, null, 2);
    const headers = new Headers();
    headers.append("content-type", "application/json");
    headers.append("X-CSRFToken", form.csrfmiddlewaretoken.value);
    const options = {
        method: "POST",
        headers: headers,
        body: dataJSON
    };

    req(url, options);
}

function onDelete(event) {
    event.preventDefault();
    const form = event.target;
    const url = form.action;
    const headers = new Headers();
    headers.append("X-CSRFToken", form.csrfmiddlewaretoken.value);
    const options = {
        method: "POST",
        headers: headers,
        body: {}
    };

    req(url, options);
}

function onOpenCloseModalDelete(event) {
    event.preventDefault();
    const modal = document.querySelector("#modal_delete");
    const display = modal.computedStyleMap.display;
    modal.computedStyleMap.display = display == "block" ? "none" : "block";
}

function onOpenCloseSidenav(event) {
    event.preventDefault();
    const sidenav = document.querySelector("#sidenav");
    const opacity = sidenav.style.opacity;
    const left = sidenav.style.left;
    sidenav.style.opacity = opacity == "1" ? "0" : "1";
    sidenav.style.left = left == "0%" ? "-100%" : "0%";
}

function onOpenCloseSearchbar(event) {
    event.preventDefault();
    const searchbar = document.querySelector("#searchbar");
    const opacity = searchbar.style.opacity;
    const right = searchbar.style.right;
    searchbar.style.opacity = opacity == "1" ? "0" : "1";
    searchbar.style.right = right == "0%" ? "-100%" : "0%";
}
