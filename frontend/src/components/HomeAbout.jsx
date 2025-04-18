import { Link } from "react-router-dom"

const HomeAbout = () => {
  return (
    <section className="home-about-section">
      <div className="home-about-container">
        <div className="home-about-content">
          <div className="home-about-text">
            <h2 className="home-about-title">About CarValue Predictor</h2>
            <p className="home-about-description">
              CarValue Predictor is a modern web application designed to provide accurate price estimates for used cars.
              Using machine learning algorithms and a comprehensive dataset of vehicle sales, our system analyzes
              multiple factors to generate market-relevant valuations.
            </p>
            <p className="home-about-description">
              Our prediction engine is continuously improving as we gather more data and refine our algorithms, making
              our estimates increasingly accurate over time.
            </p>
            <div className="home-about-features">
              <div className="home-about-feature">
                <div className="home-about-feature-icon">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <span>Advanced ML Algorithms</span>
              </div>
              <div className="home-about-feature">
                <div className="home-about-feature-icon">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <span>Comprehensive Data Analysis</span>
              </div>
              <div className="home-about-feature">
                <div className="home-about-feature-icon">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <span>Real-time Market Insights</span>
              </div>
            </div>
            <Link to="/about" className="home-about-button">
              Learn More About Us
            </Link>
          </div>
          <div className="home-about-image">
            <img
              src="https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=500&h=500"
              alt="Data analyst working on car price predictions"
              onError={(e) => {
                e.target.onerror = null
                e.target.src = "https://via.placeholder.com/500x500?text=Our+Team"
              }}
            />
          </div>
        </div>
      </div>
    </section>
  )
}

export default HomeAbout
