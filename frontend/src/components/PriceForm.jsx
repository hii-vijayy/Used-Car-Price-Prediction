"use client"

import { useState } from "react"

const PriceForm = ({ onPredictionResult }) => {
  const [formData, setFormData] = useState({
    brand: "Toyota",
    model: "Corolla",
    year: 2018,
    fuel: "Petrol",
    transmission: "Manual",
    kms_driven: 45000,
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: name === "year" || name === "kms_driven" ? Number(value) : value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Fixed API endpoint to match the Flask backend
      const apiUrl = import.meta.env.VITE_API_URL;

      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()

      // Create a result object that includes both the prediction and input data
      const result = {
        prediction: data.price,
        input: formData,
      }

      onPredictionResult(result)
    } catch (err) {
      setError("Failed to get prediction. Please try again.")
      console.error("Prediction error:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="price-form-container">
      <h2 className="form-title">Car Details</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Brand</label>
          <select name="brand" value={formData.brand} onChange={handleChange} className="form-input" required>
            <option value="Toyota">Toyota</option>
            <option value="Honda">Honda</option>
            <option value="Ford">Ford</option>
            <option value="Hyundai">Hyundai</option>
            <option value="Maruti">Maruti</option>
            <option value="BMW">BMW</option>
            <option value="Mercedes">Mercedes</option>
            <option value="Audi">Audi</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Model</label>
          <select name="model" value={formData.model} onChange={handleChange} className="form-input" required>
            <option value="Corolla">Corolla</option>
            <option value="Civic">Civic</option>
            <option value="Focus">Focus</option>
            <option value="i20">i20</option>
            <option value="Swift">Swift</option>
            <option value="3 Series">3 Series</option>
            <option value="C-Class">C-Class</option>
            <option value="A4">A4</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Manufacturing Year</label>
          <input
            type="number"
            name="year"
            min="1990"
            max="2025"
            value={formData.year}
            onChange={handleChange}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Kilometers Driven</label>
          <input
            type="number"
            name="kms_driven"
            min="0"
            max="500000"
            value={formData.kms_driven}
            onChange={handleChange}
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Fuel Type</label>
          <select name="fuel" value={formData.fuel} onChange={handleChange} className="form-input" required>
            <option value="Petrol">Petrol</option>
            <option value="Diesel">Diesel</option>
            <option value="CNG">CNG</option>
            <option value="LPG">LPG</option>
            <option value="Electric">Electric</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Transmission</label>
          <select
            name="transmission"
            value={formData.transmission}
            onChange={handleChange}
            className="form-input"
            required
          >
            <option value="Manual">Manual</option>
            <option value="Automatic">Automatic</option>
          </select>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? "Calculating..." : "Estimate Price"}
        </button>
      </form>
    </div>
  )
}

export default PriceForm
