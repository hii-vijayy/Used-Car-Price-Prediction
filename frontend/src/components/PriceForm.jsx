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

  const validateForm = () => {
    // Basic form validation
    if (!formData.brand || !formData.model || !formData.fuel || !formData.transmission) {
      return false
    }
    
    if (!formData.year || formData.year < 1990 || formData.year > new Date().getFullYear()) {
      return false
    }
    
    if (formData.kms_driven < 0 || formData.kms_driven > 1000000) {
      return false
    }
    
    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validate form before submission
    if (!validateForm()) {
      setError("Please fill all fields with valid values")
      return
    }
    
    setLoading(true)
    setError(null)

    try {
      // Get API URL from environment variables
      const apiUrl = import.meta.env.VITE_API_URL

      // First check API health if possible
      try {
        const healthCheck = await fetch(`${apiUrl}/health`, {
          method: "GET",
          signal: AbortSignal.timeout(5000) // 5 second timeout for health check
        })
        
        if (!healthCheck.ok) {
          console.warn("API health check failed, but continuing with prediction attempt")
        } else {
          const healthData = await healthCheck.json()
          console.log("API health status:", healthData)
        }
      } catch (healthError) {
        console.warn("Health check failed:", healthError)
        // Continue anyway - health check failure shouldn't block prediction attempt
      }

      // Prepare the request with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 30000) // 30 second timeout

      const response = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId) // Clear timeout if request completes

      // Handle non-200 responses with better error reporting
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: `HTTP error! Status: ${response.status}` }))
        throw new Error(errorData.error || `Server returned: ${response.status}`)
      }

      const data = await response.json()
      
      // Check if the API returned an error status
      if (data.status === "error") {
        throw new Error(data.error || "Unknown prediction error")
      }

      // Create a result object that includes both the prediction and input data
      const result = {
        prediction: data.price,
        input: formData,
        currency: data.currency || "INR"
      }

      // Pass result to parent component
      onPredictionResult(result)
    } catch (err) {
      // Handle different error types
      if (err.name === "AbortError") {
        setError("Request timed out. The server might be busy, please try again.")
      } else if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
        setError("Network error. Please check your connection and try again.")
      } else {
        setError(`Failed to get prediction: ${err.message}`)
      }
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