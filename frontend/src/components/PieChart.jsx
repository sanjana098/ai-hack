import React from "react";
import Chart from "chart.js/auto";
import { Pie } from "react-chartjs-2";

const PieChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/chances")
      .then((response) => response.json())
      .then((data) => {
        const content = data.response.choices[0].message.content;
        const dict = JSON.parse(content);
        const labels = Object.keys(dict);
        const values = Object.values(dict);
        console.log(labels);
        console.log(values);

        setChartData({
          labels: labels,
          datasets: [
            {
              label: "My First dataset",
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
                "rgb(75, 192, 192)",
                "rgb(153, 102, 255)",
                "rgb(255, 159, 64)",
                "rgb(54, 162, 235)"
              ],
              borderColor: "rgb(0, 0, 255)",
              data: values
            }
          ]
        });
      });
  }, []);

  return (
    <div>
      {chartData && <Pie data={chartData} />}
    </div>
  );
};

export default PieChart;
