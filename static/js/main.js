

function writeToTable(data){
    var table = document.getElementById('resultTable')
    var columns = ["Email", "Rating", "Color", "Comment"]
    var tr = table.insertRow(-1);                   // TABLE ROW.

    for (var i = 0; i < columns.length; i++) {
        var th = document.createElement("th");      // TABLE HEADER.
        th.innerHTML = columns[i];
        tr.appendChild(th);
    }

    // ADD JSON DATA TO THE TABLE AS ROWS.
    for (var i = 0; i < data.length; i++) {

        tr = table.insertRow(-1);
        var tabCell = tr.insertCell(-1);
        const email = data[i]["email"]
        tabCell.innerHTML = email
        tabCell = tr.insertCell(-1);
        const rating = data[i]["rating"]
        tabCell.innerHTML = rating
        tabCell = tr.insertCell(-1);
        const color = data[i]["color"]
        tabCell.innerHTML = color
        tabCell = tr.insertCell(-1);
        const comment = data[i]["comment"]
        tabCell.innerHTML = comment

    }
}

window.onload = function() {

    document.getElementById('submitBtn').onclick = function() {
        console.log("workig")
        const date = document.getElementById("email").value
        console.log(date)
        $.ajax({
            url: '/data',
            type: 'post',
            data: date,
            headers: {
                "Content-type": 'application/json; charset=utf-8',
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                writeToTable([data])
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("error")
                console.log('Error: '+jqXHR+' '+textStatus+' '+errorThrown);
            }
        });
        return false;
    };
};

