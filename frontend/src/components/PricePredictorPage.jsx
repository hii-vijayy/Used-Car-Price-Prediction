"use client"

import { useState } from "react"
import PriceForm from "./PriceForm"
import PriceDisplay from "./PriceDisplay"

const PricePredictorPage = () => {
  const [predictionResult, setPredictionResult] = useState(null)

  return (
    <div className="predictor-container">
      <div className="predictor-header">
        <h1 className="predictor-title">Used Car Price Estimator</h1>
        <p className="predictor-description">
          Get an accurate market value for your used car based on ML-powered analysis
        </p>
      </div>

      <div className="predictor-content">
        <div className="form-section">
          <PriceForm onPredictionResult={setPredictionResult} />

          <div className="predictor-tips">
            <h3 className="tips-title">Tips for Accurate Estimates</h3>
            <ul className="tips-list">
              <li>Enter the exact year of manufacture</li>
              <li>Provide accurate mileage information</li>
              <li>Select the correct transmission type</li>
              <li>Choose the appropriate fuel type</li>
            </ul>
          </div>
        </div>
        <div className="result-section">
          {predictionResult ? (
            <PriceDisplay result={predictionResult} />
          ) : (
            <div className="empty-result">
              <div className="empty-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  ></path>
                </svg>
              </div>
              <h3 className="empty-title">Fill out the form</h3>
              <p className="empty-description">Enter your car details to get an estimated price</p>
              <div className="empty-features">
                <div className="empty-feature">
                  <span className="empty-feature-icon">✓</span>
                  <span>Instant valuation</span>
                </div>
                <div className="empty-feature">
                  <span className="empty-feature-icon">✓</span>
                  <span>Market comparison</span>
                </div>
                <div className="empty-feature">
                  <span className="empty-feature-icon">✓</span>
                  <span>Price breakdown</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default PricePredictorPage
