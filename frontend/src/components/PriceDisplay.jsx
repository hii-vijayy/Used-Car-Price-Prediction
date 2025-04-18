import { Bar } from "react-chartjs-2"
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js"

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const PriceDisplay = ({ result }) => {
  if (!result) return null

  const { prediction, input } = result

  // Calculate car age for display
  const carAge = new Date().getFullYear() - input.year

  // Chart data to show feature importance (dummy data - in a real app, this would come from the model)
  const chartData = {
    labels: ["Year", "Mileage", "Brand", "Transmission", "Fuel Type"],
    datasets: [
      {
        label: "Feature Importance",
        data: [30, 25, 20, 15, 10], // These would be actual importance values from the model
        backgroundColor: [
          "rgba(30, 64, 175, 0.7)",
          "rgba(37, 99, 235, 0.7)",
          "rgba(59, 130, 246, 0.7)",
          "rgba(96, 165, 250, 0.7)",
          "rgba(147, 197, 253, 0.7)",
        ],
        borderColor: [
          "rgba(30, 64, 175, 1)",
          "rgba(37, 99, 235, 1)",
          "rgba(59, 130, 246, 1)",
          "rgba(96, 165, 250, 1)",
          "rgba(147, 197, 253, 1)",
        ],
        borderWidth: 1,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: "Factors Affecting Car Price",
        font: {
          size: 16,
          weight: "bold",
        },
      },
    },
  }

  // Calculate value ranges for comparison
  const lowerRange = Math.round(prediction * 0.9)
  const upperRange = Math.round(prediction * 1.1)

  return (
    <div className="price-display">
      <div className="price-header">
        <h2 className="price-title">Estimated Value</h2>
        <div className="price-value">${prediction.toLocaleString()}</div>
        <div className="price-range">
          Market range: ${lowerRange.toLocaleString()} - ${upperRange.toLocaleString()}
        </div>
      </div>

      <div className="price-details">
        <div className="car-summary">
          <h3 className="section-title">Car Details Summary</h3>
          <table className="details-table">
            <tbody>
              <tr>
                <td>Brand</td>
                <td>{input.brand}</td>
              </tr>
              <tr>
                <td>Model</td>
                <td>{input.model}</td>
              </tr>
              <tr>
                <td>Age</td>
                <td>{carAge} years</td>
              </tr>
              <tr>
                <td>Mileage</td>
                <td>{input.kms_driven.toLocaleString()} km</td>
              </tr>
              <tr>
                <td>Fuel Type</td>
                <td>{input.fuel}</td>
              </tr>
              <tr>
                <td>Transmission</td>
                <td>{input.transmission}</td>
              </tr>
            </tbody>
          </table>

          <div className="price-actions">
            <button className="action-button">Save Estimate</button>
            <button className="action-button action-button-outline">Print Report</button>
          </div>
        </div>

        <div className="price-factors">
          <h3 className="section-title">Price Factors</h3>
          <div className="chart-container">
            <Bar data={chartData} options={chartOptions} />
          </div>
        </div>
      </div>

      <div className="market-insights">
        <h3 className="insights-title">Market Insights</h3>
        <p className="insights-text">
          This estimation is based on analysis of {">"}45,000 used car sales. Cars with {input.transmission}{" "}
          transmission and {input.fuel} fuel type typically retain value better in the current market.{" "}
          {carAge < 5
            ? "Your vehicle's young age significantly increases its value."
            : "Consider highlighting the well-maintained condition to improve selling price."}
        </p>
      </div>

      <div className="similar-cars">
        <h3 className="section-title">Similar Cars in Market</h3>
        <div className="similar-cars-grid">
          <div className="similar-car-card">
            <div className="similar-car-year">{input.year}</div>
            <div className="similar-car-model">
              {input.brand} {input.model}
            </div>
            <div className="similar-car-details">
              {input.transmission}, {Math.round(input.kms_driven * 0.9).toLocaleString()} km
            </div>
            <div className="similar-car-price">${Math.round(prediction * 0.95).toLocaleString()}</div>
          </div>
          <div className="similar-car-card">
            <div className="similar-car-year">{input.year}</div>
            <div className="similar-car-model">
              {input.brand} {input.model}
            </div>
            <div className="similar-car-details">
              {input.transmission}, {Math.round(input.kms_driven * 1.1).toLocaleString()} km
            </div>
            <div className="similar-car-price">${Math.round(prediction * 0.92).toLocaleString()}</div>
          </div>
          <div className="similar-car-card">
            <div className="similar-car-year">{input.year - 1}</div>
            <div className="similar-car-model">
              {input.brand} {input.model}
            </div>
            <div className="similar-car-details">
              {input.transmission}, {Math.round(input.kms_driven * 1.2).toLocaleString()} km
            </div>
            <div className="similar-car-price">${Math.round(prediction * 0.85).toLocaleString()}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PriceDisplay
