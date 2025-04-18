import { Link } from "react-router-dom"
import HomeAbout from "./HomeAbout"
import TestimonialSection from "./TestimonialSection"
import CarBrands from "./CarBrands"

const HomePage = () => {
  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">Find Your Car's True Value</h1>
            <p className="hero-description">
              Our advanced machine learning algorithm analyzes thousands of car sales to provide you with an accurate
              market value for your vehicle in seconds.
            </p>
            <div className="hero-buttons">
              <Link to="/predictor" className="hero-button">
                Get Started
              </Link>
              <a href="#how-it-works" className="hero-button-secondary">
                Learn More
              </a>
            </div>
          </div>
          <div className="hero-image">
            <img
              src="https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=500&h=300"
              alt="Car value illustration"
              onError={(e) => {
                e.target.onerror = null
                e.target.src = "https://via.placeholder.com/500x300?text=Car+Value+Predictor"
              }}
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          <div className="stat-item">
            <div className="stat-value">45,000+</div>
            <div className="stat-label">Car Sales Analyzed</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">98%</div>
            <div className="stat-label">Prediction Accuracy</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">15,000+</div>
            <div className="stat-label">Happy Users</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">24/7</div>
            <div className="stat-label">Available Service</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">Why Choose Our Car Value Predictor?</h2>

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                ></path>
              </svg>
            </div>
            <h3 className="feature-title">ML-Powered Accuracy</h3>
            <p className="feature-description">
              Our model is trained on 45,000+ real car sales data points, providing you with market-accurate valuations.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </div>
            <h3 className="feature-title">Instant Results</h3>
            <p className="feature-description">
              Get your car's estimated value in seconds, no lengthy forms or waiting periods required.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                ></path>
              </svg>
            </div>
            <h3 className="feature-title">Detailed Analysis</h3>
            <p className="feature-description">
              Understand exactly which factors affect your car's value with our detailed price breakdown.
            </p>
          </div>
        </div>
      </section>

      {/* Car Brands Section */}
      <CarBrands />

      {/* How It Works Section */}
      <section className="how-it-works" id="how-it-works">
        <h2 className="section-title">How It Works</h2>

        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3 className="step-title">Enter Your Car Details</h3>
              <p className="step-description">
                Provide basic information about your car including year, mileage, engine size and more.
              </p>
            </div>
          </div>

          <div className="step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3 className="step-title">Our ML Model Processes Data</h3>
              <p className="step-description">
                Our advanced algorithm analyzes your car's features against thousands of similar vehicles.
              </p>
            </div>
          </div>

          <div className="step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3 className="step-title">Get Your Valuation</h3>
              <p className="step-description">
                Receive an accurate price estimate along with insights into what factors affect your car's value.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* About Section on Home Page */}
      <HomeAbout />

      {/* Testimonials Section */}
      <TestimonialSection />

      {/* CTA Section */}
      <section className="cta-section">
        <h2 className="cta-title">Ready to Discover Your Car's Value?</h2>
        <p className="cta-description">
          Whether you're selling, trading in, or just curious about your car's worth, our predictor gives you the
          insights you need to make informed decisions.
        </p>
        <Link to="/predictor" className="cta-button">
          Try It Now
        </Link>
      </section>
    </div>
  )
}

export default HomePage
