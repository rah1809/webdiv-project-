// script.js
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const uploadButton = document.getElementById("upload-button");
    const dataTable = document.getElementById("data-table-view");
    const dataChartCanvas = document.getElementById("data-chart");
  
    let dataset = [];
  
    // Handle File Upload
    uploadButton.addEventListener("click", () => {
      const file = fileInput.files[0];
      if (!file) {
        alert("Please select a CSV file to upload.");
        return;
      }
  
      const reader = new FileReader();
      reader.onload = (event) => {
        const csvData = event.target.result;
        dataset = parseCSV(csvData);
        renderTable(dataset);
        renderChart(dataset);
      };
      reader.readAsText(file);
    });
  
    // Parse CSV to Array of Objects
    const parseCSV = (csv) => {
      const lines = csv.split("\n").filter((line) => line.trim() !== "");
      const headers = lines[0].split(",");
      return lines.slice(1).map((line) => {
        const values = line.split(",");
        return headers.reduce((obj, header, index) => {
          obj[header.trim()] = values[index].trim();
          return obj;
        }, {});
      });
    };
  
    // Render Data Table
    const renderTable = (data) => {
      dataTable.innerHTML = "";
      if (data.length === 0) return;
  
      // Add headers
      const headers = Object.keys(data[0]);
      const headerRow = document.createElement("tr");
      headers.forEach((header) => {
        const th = document.createElement("th");
        th.textContent = header;
        headerRow.appendChild(th);
      });
      dataTable.appendChild(headerRow);
  
      // Add rows
      data.forEach((row) => {
        const tr = document.createElement("tr");
        headers.forEach((header) => {
          const td = document.createElement("td");
          td.textContent = row[header];
          tr.appendChild(td);
        });
        dataTable.appendChild(tr);
      });

    };
  
    // Render Chart
    const renderChart = (data) => {
      console.log("chart data >>",data)
      if (data.length === 0) return;
  
      // Use first two columns for chart
      const labels = data.map((row) => row[Object.keys(row)[0]]);
      const values = data.map((row) => {
        console.log("row item",row[Object.keys(row)[1]])
        parseFloat(row[Object.keys(row)[1]]) || 0);
      }
      console.log("labels >>", labels)
      console.log("values >>", values)
      new Chart(dataChartCanvas, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Data Analysis",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    };
  });
  