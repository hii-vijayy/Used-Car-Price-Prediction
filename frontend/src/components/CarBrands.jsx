const CarBrands = () => {
    const brands = [
      { name: "Toyota", logo: "https://www.carlogos.org/car-logos/toyota-logo-2020-europe-640.png" },
      { name: "Honda", logo: "https://www.carlogos.org/car-logos/honda-logo-2000-full-640.png" },
      { name: "Ford", logo: "https://www.carlogos.org/car-logos/ford-logo-2017-640.png" },
      { name: "BMW", logo: "https://www.carlogos.org/car-logos/bmw-logo-2020-gray.png" },
      { name: "Mercedes", logo: "https://www.carlogos.org/logo/Mercedes-Benz-logo-2011-640x369.jpg" },
      { name: "Audi", logo: "https://www.carlogos.org/car-logos/audi-logo-2016-640.png" },
    ]
  
    return (
      <section className="brands-section">
        <h2 className="brands-title">Supported Car Brands</h2>
        <p className="brands-description">Our prediction model supports all major car manufacturers</p>
  
        <div className="brands-container">
          {brands.map((brand, index) => (
            <div key={index} className="brand-item">
              <img
                src={brand.logo || "/placeholder.svg"}
                alt={`${brand.name} logo`}
                className="brand-logo"
                onError={(e) => {
                  e.target.onerror = null
                  e.target.src = `https://via.placeholder.com/120x80?text=${brand.name}`
                }}
              />
            </div>
          ))}
        </div>
      </section>
    )
  }
  
  export default CarBrands
  