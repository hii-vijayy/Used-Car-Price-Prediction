const TestimonialSection = () => {
    const testimonials = [
      {
        id: 1,
        name: "Sarah Johnson",
        role: "Car Seller",
        image: "https://randomuser.me/api/portraits/women/32.jpg",
        quote:
          "CarValue Predictor gave me an accurate estimate that helped me negotiate a better price when selling my Toyota Corolla. The detailed breakdown of factors affecting the price was incredibly helpful!",
      },
      {
        id: 2,
        name: "Michael Chen",
        role: "Car Buyer",
        image: "https://randomuser.me/api/portraits/men/45.jpg",
        quote:
          "I was skeptical about online car valuations until I tried CarValue Predictor. The estimate was within $300 of what the dealer offered, which gave me confidence during negotiations.",
      },
      {
        id: 3,
        name: "Emily Rodriguez",
        role: "Car Dealer",
        image: "https://randomuser.me/api/portraits/women/68.jpg",
        quote:
          "As a used car dealer, I rely on accurate valuations daily. This tool has become an essential part of our business process. The ML-powered predictions are consistently reliable.",
      },
    ]
  
    return (
      <section className="testimonial-section">
        <h2 className="section-title">What Our Users Say</h2>
  
        <div className="testimonial-container">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="testimonial-card">
              <div className="testimonial-content">
                <div className="testimonial-quote">
                  <svg className="quote-icon" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                  </svg>
                  <p className="testimonial-text">{testimonial.quote}</p>
                </div>
                <div className="testimonial-author">
                  <img
                    src={testimonial.image || "/placeholder.svg"}
                    alt={testimonial.name}
                    className="testimonial-image"
                    onError={(e) => {
                      e.target.onerror = null
                      e.target.src = `https://via.placeholder.com/60x60?text=${testimonial.name.charAt(0)}`
                    }}
                  />
                  <div className="testimonial-info">
                    <h4 className="testimonial-name">{testimonial.name}</h4>
                    <p className="testimonial-role">{testimonial.role}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    )
  }
  
  export default TestimonialSection
  