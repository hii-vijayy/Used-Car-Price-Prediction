import { Link } from "react-router-dom"
import "../App.css"

const AboutPage = () => {
  return (
    <div className="about-container">
      <div className="about-header">
        <h1 className="about-title">About CarValue Predictor</h1>
        <p className="about-subtitle">Learn about our project, technology, and team</p>
      </div>

      {/* About the Project */}
      <section className="about-section">
        <h2 className="section-title">The Project</h2>
        <p className="section-text">
          CarValue Predictor is a modern web application designed to provide accurate price estimates for used cars.
          Using machine learning algorithms and a comprehensive dataset of vehicle sales, our system analyzes multiple
          factors to generate market-relevant valuations.
        </p>
        <p className="section-text">
          We built this project to help car owners, buyers, and sellers make informed decisions by providing
          transparent, data-driven price estimates that reflect current market conditions.
        </p>
        <p className="section-text">
          Our prediction engine is continuously improving as we gather more data and refine our algorithms, making our
          estimates increasingly accurate over time.
        </p>
      </section>

      {/* Technology Stack */}
      <section className="about-section">
        <h2 className="section-title">Our Technology</h2>

        <div className="tech-grid">
          <div className="tech-column">
            <h3 className="tech-title">Frontend</h3>
            <ul className="tech-list">
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                React - Modern UI library
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                Chart.js - Interactive visualizations
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                CSS3 - Responsive styling
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                Fetch API - API communication
              </li>
            </ul>
          </div>

          <div className="tech-column">
            <h3 className="tech-title">Backend</h3>
            <ul className="tech-list">
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                Flask - Python web framework
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                Apache Spark (PySpark) - Data processing
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                MLlib - Machine learning library
              </li>
              <li className="tech-item">
                <span className="tech-icon">✓</span>
                Pandas - Data analysis
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Our Models */}
      <section className="about-section">
        <h2 className="section-title">Our ML Models</h2>

        <p className="section-text">
          Our prediction system uses several machine learning models to achieve high accuracy:
        </p>

        <div className="models-list">
          <div className="model-item">
            <h3 className="model-title">Random Forest Regressor</h3>
            <p className="model-description">
              Our primary model that handles non-linear relationships and feature interactions with excellent accuracy.
            </p>
          </div>

          <div className="model-item">
            <h3 className="model-title">Linear Regression</h3>
            <p className="model-description">
              Used as a baseline and for specific vehicle segments where linear relationships are dominant.
            </p>
          </div>

          <div className="model-item">
            <h3 className="model-title">Gradient Boosting</h3>
            <p className="model-description">
              Employed for complex feature interactions and to improve prediction accuracy for luxury vehicles.
            </p>
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="about-section">
        <h2 className="section-title">Our Data</h2>

        <p className="section-text">
          We've gathered data from multiple sources to build a comprehensive training dataset:
        </p>

        <ul className="data-list">
          <li className="data-item">
            <span className="data-icon">📊</span>
            <span>45,000+ used car listings with verified sale prices</span>
          </li>
          <li className="data-item">
            <span className="data-icon">📊</span>
            <span>Vehicle specifications from manufacturer databases</span>
          </li>
          <li className="data-item">
            <span className="data-icon">📊</span>
            <span>Market trend data from automotive industry reports</span>
          </li>
        </ul>

        <p className="section-text">
          Our dataset includes vehicles from various manufacturers, model years, body types, and price segments to
          ensure comprehensive coverage.
        </p>
      </section>

      {/* CTA */}
      <section className="about-cta">
        <h2 className="cta-title">Ready to try our car price predictor?</h2>
        <Link to="/predictor" className="cta-button">
          Get Started
        </Link>
      </section>
    </div>
  )
}

export default AboutPage
