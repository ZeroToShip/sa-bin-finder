/* ============================================================
   SA Bin Finder — Store & State Data
   ============================================================ */

window.SAData = {

  /* ---- ALL 50 STATES ---- */
  states: [
    { name: "Alabama",        slug: "alabama" },
    { name: "Alaska",         slug: "alaska" },
    { name: "Arizona",        slug: "arizona" },
    { name: "Arkansas",       slug: "arkansas" },
    { name: "California",     slug: "california" },
    { name: "Colorado",       slug: "colorado" },
    { name: "Connecticut",    slug: "connecticut" },
    { name: "Delaware",       slug: "delaware" },
    { name: "Florida",        slug: "florida" },
    { name: "Georgia",        slug: "georgia" },
    { name: "Hawaii",         slug: "hawaii" },
    { name: "Idaho",          slug: "idaho" },
    { name: "Illinois",       slug: "illinois" },
    { name: "Indiana",        slug: "indiana" },
    { name: "Iowa",           slug: "iowa" },
    { name: "Kansas",         slug: "kansas" },
    { name: "Kentucky",       slug: "kentucky" },
    { name: "Louisiana",      slug: "louisiana" },
    { name: "Maine",          slug: "maine" },
    { name: "Maryland",       slug: "maryland" },
    { name: "Massachusetts",  slug: "massachusetts" },
    { name: "Michigan",       slug: "michigan" },
    { name: "Minnesota",      slug: "minnesota" },
    { name: "Mississippi",    slug: "mississippi" },
    { name: "Missouri",       slug: "missouri" },
    { name: "Montana",        slug: "montana" },
    { name: "Nebraska",       slug: "nebraska" },
    { name: "Nevada",         slug: "nevada" },
    { name: "New Hampshire",  slug: "new-hampshire" },
    { name: "New Jersey",     slug: "new-jersey" },
    { name: "New Mexico",     slug: "new-mexico" },
    { name: "New York",       slug: "new-york" },
    { name: "North Carolina", slug: "north-carolina" },
    { name: "North Dakota",   slug: "north-dakota" },
    { name: "Ohio",           slug: "ohio" },
    { name: "Oklahoma",       slug: "oklahoma" },
    { name: "Oregon",         slug: "oregon" },
    { name: "Pennsylvania",   slug: "pennsylvania" },
    { name: "Rhode Island",   slug: "rhode-island" },
    { name: "South Carolina", slug: "south-carolina" },
    { name: "South Dakota",   slug: "south-dakota" },
    { name: "Tennessee",      slug: "tennessee" },
    { name: "Texas",          slug: "texas" },
    { name: "Utah",           slug: "utah" },
    { name: "Vermont",        slug: "vermont" },
    { name: "Virginia",       slug: "virginia" },
    { name: "Washington",     slug: "washington" },
    { name: "West Virginia",  slug: "west-virginia" },
    { name: "Wisconsin",      slug: "wisconsin" },
    { name: "Wyoming",        slug: "wyoming" }
  ],

  /* ---- SAMPLE STORES ---- */
  stores: [

    /* ===== CALIFORNIA ===== */
    {
      id: "ca-001",
      name: "Salvation Army Outlet Store",
      address: "1234 W Jefferson Blvd",
      city: "Los Angeles", state: "California", slug: "california", zip: "90018",
      phone: "(323) 555-0192",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "10:00 AM – 5:00 PM"
      },
      pricing: "$1.49/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "One of LA's largest Salvation Army outlet stores with fresh bin restocks twice weekly. Huge selection of clothing, housewares, and small electronics. Arrive early on restock days for the best deals.",
      features: ["Clothing", "Housewares", "Electronics", "Books", "Toys"],
      verified: true, added: "2024-11-15"
    },
    {
      id: "ca-002",
      name: "Salvation Army Bin Store – Mission Valley",
      address: "5765 Friars Rd",
      city: "San Diego", state: "California", slug: "california", zip: "92110",
      phone: "(619) 555-0234",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 6:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Wednesday", "Saturday"],
      description: "Popular bin store in Mission Valley. Great for finding designer clothing and collectibles at rock-bottom prices. Active local reseller community.",
      features: ["Clothing", "Accessories", "Books", "Collectibles"],
      verified: true, added: "2024-12-01"
    },
    {
      id: "ca-003",
      name: "Salvation Army By-The-Pound – Bay Area",
      address: "2209 Oakdale Ave",
      city: "San Francisco", state: "California", slug: "california", zip: "94124",
      phone: "(415) 555-0311",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "11:00 AM – 4:00 PM"
      },
      pricing: "$1.79/lb",
      restock_days: ["Monday", "Thursday"],
      description: "SF's go-to bin store in the Bayview district. Known for vintage finds and a wide variety of household goods.",
      features: ["Clothing", "Vintage", "Housewares", "Electronics"],
      verified: false, added: "2025-01-10"
    },

    /* ===== TEXAS ===== */
    {
      id: "tx-001",
      name: "Salvation Army Bin Store – Houston",
      address: "8501 Irvington Blvd",
      city: "Houston", state: "Texas", slug: "texas", zip: "77022",
      phone: "(713) 555-0187",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "11:00 AM – 5:00 PM"
      },
      pricing: "$1.59/lb",
      restock_days: ["Monday", "Thursday"],
      description: "High-volume bin store with daily fresh stock. One of Houston's most popular thrift destinations for resellers and bargain hunters. Furniture and large items available on select days.",
      features: ["Clothing", "Housewares", "Electronics", "Furniture", "Toys"],
      verified: true, added: "2024-10-20"
    },
    {
      id: "tx-002",
      name: "Salvation Army Outlet – Dallas",
      address: "3891 E Illinois Ave",
      city: "Dallas", state: "Texas", slug: "texas", zip: "75216",
      phone: "(214) 555-0143",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.49/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Large Dallas outlet with excellent furniture and clothing selection. Busy on restock days — arrive early for the freshest inventory.",
      features: ["Clothing", "Furniture", "Housewares", "Books"],
      verified: true, added: "2024-11-05"
    },
    {
      id: "tx-003",
      name: "Salvation Army By-The-Pound – Austin",
      address: "5501 S Congress Ave",
      city: "Austin", state: "Texas", slug: "texas", zip: "78745",
      phone: "(512) 555-0248",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 8:00 PM", "Saturday": "8:00 AM – 8:00 PM",
        "Sunday": "10:00 AM – 5:00 PM"
      },
      pricing: "$1.39/lb",
      restock_days: ["Wednesday", "Saturday"],
      description: "Austin's creative crowd loves this bin store for vintage finds and eclectic housewares. Great variety every restock day.",
      features: ["Vintage", "Clothing", "Books", "Housewares", "Collectibles"],
      verified: true, added: "2025-01-25"
    },

    /* ===== FLORIDA ===== */
    {
      id: "fl-001",
      name: "Salvation Army Bin Store – Miami",
      address: "2801 NW 7th Ave",
      city: "Miami", state: "Florida", slug: "florida", zip: "33127",
      phone: "(305) 555-0219",
      hours: {
        "Monday": "9:00 AM – 7:00 PM", "Tuesday": "9:00 AM – 7:00 PM",
        "Wednesday": "9:00 AM – 7:00 PM", "Thursday": "9:00 AM – 7:00 PM",
        "Friday": "9:00 AM – 8:00 PM", "Saturday": "8:00 AM – 8:00 PM",
        "Sunday": "10:00 AM – 6:00 PM"
      },
      pricing: "$1.69/lb",
      restock_days: ["Monday", "Wednesday", "Friday"],
      description: "Miami's busiest SA bin store with three restocks per week. Huge variety of tropical clothing and diverse household items. Extended hours on weekends.",
      features: ["Clothing", "Accessories", "Housewares", "Electronics", "Toys"],
      verified: true, added: "2024-09-30"
    },
    {
      id: "fl-002",
      name: "Salvation Army Outlet – Orlando",
      address: "4595 N Orange Blossom Trl",
      city: "Orlando", state: "Florida", slug: "florida", zip: "32804",
      phone: "(407) 555-0176",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "12:00 PM – 5:00 PM"
      },
      pricing: "$1.49/lb",
      restock_days: ["Tuesday", "Saturday"],
      description: "Centrally located bin store near downtown Orlando. Known for excellent toy and electronics finds — popular with Disney workers.",
      features: ["Clothing", "Toys", "Electronics", "Books", "Housewares"],
      verified: true, added: "2024-12-10"
    },

    /* ===== NEW YORK ===== */
    {
      id: "ny-001",
      name: "Salvation Army Bin Store – Brooklyn",
      address: "2395 Pitkin Ave",
      city: "Brooklyn", state: "New York", slug: "new-york", zip: "11207",
      phone: "(718) 555-0254",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "11:00 AM – 5:00 PM"
      },
      pricing: "$1.99/lb",
      restock_days: ["Monday", "Thursday"],
      description: "NYC's premier SA bin store. High demand means excellent turnover. Expect lines on restock days — come before opening for the best finds. Reseller-friendly.",
      features: ["Clothing", "Accessories", "Books", "Housewares"],
      verified: true, added: "2024-10-05"
    },
    {
      id: "ny-002",
      name: "Salvation Army Outlet – Buffalo",
      address: "960 Broadway",
      city: "Buffalo", state: "New York", slug: "new-york", zip: "14212",
      phone: "(716) 555-0118",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 6:00 PM", "Saturday": "9:00 AM – 6:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Wednesday", "Saturday"],
      description: "Buffalo's go-to bin store with very affordable pricing. Great winter clothing selection year-round due to the local climate.",
      features: ["Clothing", "Winter Wear", "Books", "Housewares"],
      verified: false, added: "2025-01-10"
    },

    /* ===== GEORGIA ===== */
    {
      id: "ga-001",
      name: "Salvation Army Bin Store – Atlanta",
      address: "500 Northside Dr NW",
      city: "Atlanta", state: "Georgia", slug: "georgia", zip: "30318",
      phone: "(404) 555-0301",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "12:00 PM – 5:00 PM"
      },
      pricing: "$1.39/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Atlanta's largest SA outlet. Excellent clothing and housewares with affordable per-pound pricing. Located near the Westside.",
      features: ["Clothing", "Housewares", "Electronics", "Books", "Furniture"],
      verified: true, added: "2024-11-20"
    },
    {
      id: "ga-002",
      name: "Salvation Army Outlet – Savannah",
      address: "1901 E Victory Dr",
      city: "Savannah", state: "Georgia", slug: "georgia", zip: "31404",
      phone: "(912) 555-0145",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 6:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Savannah's hidden gem bin store. Great variety of antiques, clothing, and Southern goods at excellent prices.",
      features: ["Clothing", "Antiques", "Housewares", "Books"],
      verified: true, added: "2025-02-05"
    },

    /* ===== ILLINOIS ===== */
    {
      id: "il-001",
      name: "Salvation Army Outlet – Chicago",
      address: "5040 W Chicago Ave",
      city: "Chicago", state: "Illinois", slug: "illinois", zip: "60651",
      phone: "(773) 555-0267",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "11:00 AM – 5:00 PM"
      },
      pricing: "$1.59/lb",
      restock_days: ["Monday", "Friday"],
      description: "Chicago's premier bin store on the West Side. High volume with great variety of clothing and housewares. Huge reseller community.",
      features: ["Clothing", "Housewares", "Electronics", "Books", "Collectibles"],
      verified: true, added: "2024-10-15"
    },

    /* ===== OHIO ===== */
    {
      id: "oh-001",
      name: "Salvation Army Bin Store – Columbus",
      address: "1161 W Broad St",
      city: "Columbus", state: "Ohio", slug: "ohio", zip: "43222",
      phone: "(614) 555-0148",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 6:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Wednesday", "Saturday"],
      description: "Columbus's most popular SA bin store. Known for excellent household finds and one of the most affordable per-pound prices in Ohio.",
      features: ["Clothing", "Housewares", "Toys", "Books", "Electronics"],
      verified: true, added: "2024-12-05"
    },
    {
      id: "oh-002",
      name: "Salvation Army Outlet – Cleveland",
      address: "4501 Lorain Ave",
      city: "Cleveland", state: "Ohio", slug: "ohio", zip: "44102",
      phone: "(216) 555-0193",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.39/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Cleveland's West Side bin store with a loyal community of shoppers. Great for vintage and retro finds.",
      features: ["Clothing", "Vintage", "Housewares", "Electronics"],
      verified: false, added: "2025-01-18"
    },

    /* ===== PENNSYLVANIA ===== */
    {
      id: "pa-001",
      name: "Salvation Army Outlet – Philadelphia",
      address: "3523 Kensington Ave",
      city: "Philadelphia", state: "Pennsylvania", slug: "pennsylvania", zip: "19134",
      phone: "(215) 555-0183",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.49/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Philly's top bin store destination. Active reseller community and great clothing selection year-round. Bin prices drop toward end of week.",
      features: ["Clothing", "Accessories", "Books", "Housewares"],
      verified: true, added: "2024-11-01"
    },

    /* ===== MICHIGAN ===== */
    {
      id: "mi-001",
      name: "Salvation Army By-The-Pound – Detroit",
      address: "3031 Grand River Ave",
      city: "Detroit", state: "Michigan", slug: "michigan", zip: "48208",
      phone: "(313) 555-0229",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "12:00 PM – 5:00 PM"
      },
      pricing: "$1.39/lb",
      restock_days: ["Monday", "Thursday"],
      description: "Detroit's best bin store near downtown. Excellent vintage clothing and collectibles. Very popular with resellers — the bins move fast on restock days.",
      features: ["Clothing", "Vintage", "Collectibles", "Housewares", "Electronics"],
      verified: true, added: "2024-09-15"
    },
    {
      id: "mi-002",
      name: "Salvation Army Bin Store – Grand Rapids",
      address: "1491 Division Ave S",
      city: "Grand Rapids", state: "Michigan", slug: "michigan", zip: "49507",
      phone: "(616) 555-0156",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.89/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Grand Rapids' flagship by-the-pound outlet. All items from area SA thrift stores that don't sell are brought here. Fresh stock twice weekly at $1.89/lb.",
      features: ["Clothing", "Housewares", "Books", "Electronics", "Toys"],
      verified: true, added: "2025-02-01"
    },

    /* ===== ARIZONA ===== */
    {
      id: "az-001",
      name: "Salvation Army Bin Store – Phoenix",
      address: "2702 W McDowell Rd",
      city: "Phoenix", state: "Arizona", slug: "arizona", zip: "85009",
      phone: "(602) 555-0274",
      hours: {
        "Monday": "9:00 AM – 7:00 PM", "Tuesday": "9:00 AM – 7:00 PM",
        "Wednesday": "9:00 AM – 7:00 PM", "Thursday": "9:00 AM – 7:00 PM",
        "Friday": "9:00 AM – 8:00 PM", "Saturday": "8:00 AM – 8:00 PM",
        "Sunday": "10:00 AM – 5:00 PM"
      },
      pricing: "$1.49/lb",
      restock_days: ["Monday", "Wednesday", "Friday"],
      description: "Phoenix's busiest SA bin store with 3 restocks per week. Extended hours and great for high-volume resellers. Large footprint with plenty of bins.",
      features: ["Clothing", "Housewares", "Electronics", "Toys", "Books"],
      verified: true, added: "2024-10-25"
    },
    {
      id: "az-002",
      name: "Salvation Army Outlet – Tucson",
      address: "140 W Silverlake Rd",
      city: "Tucson", state: "Arizona", slug: "arizona", zip: "85713",
      phone: "(520) 555-0198",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Tuesday", "Saturday"],
      description: "Tucson's top bin store with excellent pricing. Popular with university students and vintage clothing enthusiasts. Quieter than Phoenix — great for a relaxed dig.",
      features: ["Clothing", "Vintage", "Books", "Housewares"],
      verified: false, added: "2025-01-20"
    },

    /* ===== TENNESSEE ===== */
    {
      id: "tn-001",
      name: "Salvation Army Bin Store – Nashville",
      address: "636 Murfreesboro Pike",
      city: "Nashville", state: "Tennessee", slug: "tennessee", zip: "37210",
      phone: "(615) 555-0337",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.29/lb",
      restock_days: ["Monday", "Thursday"],
      description: "Nashville's most popular bin store. Great for vintage western wear, boots, and country style clothing. A reseller favorite in Music City.",
      features: ["Clothing", "Western Wear", "Boots", "Housewares", "Books"],
      verified: true, added: "2024-12-18"
    },

    /* ===== WASHINGTON ===== */
    {
      id: "wa-001",
      name: "Salvation Army Outlet – Seattle",
      address: "1010 4th Ave S",
      city: "Seattle", state: "Washington", slug: "washington", zip: "98134",
      phone: "(206) 555-0441",
      hours: {
        "Monday": "9:00 AM – 7:00 PM", "Tuesday": "9:00 AM – 7:00 PM",
        "Wednesday": "9:00 AM – 7:00 PM", "Thursday": "9:00 AM – 7:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "9:00 AM – 7:00 PM",
        "Sunday": "11:00 AM – 5:00 PM"
      },
      pricing: "$1.69/lb",
      restock_days: ["Tuesday", "Friday"],
      description: "Seattle's premier SA outlet near SoDo. Popular with tech workers hunting for deals. Great outdoor gear and quality clothing finds.",
      features: ["Clothing", "Outdoor Gear", "Electronics", "Books", "Housewares"],
      verified: true, added: "2024-11-30"
    },

    /* ===== NORTH CAROLINA ===== */
    {
      id: "nc-001",
      name: "Salvation Army Bin Store – Charlotte",
      address: "3007 Freedom Dr",
      city: "Charlotte", state: "North Carolina", slug: "north-carolina", zip: "28208",
      phone: "(704) 555-0512",
      hours: {
        "Monday": "9:00 AM – 6:00 PM", "Tuesday": "9:00 AM – 6:00 PM",
        "Wednesday": "9:00 AM – 6:00 PM", "Thursday": "9:00 AM – 6:00 PM",
        "Friday": "9:00 AM – 7:00 PM", "Saturday": "8:00 AM – 7:00 PM",
        "Sunday": "Closed"
      },
      pricing: "$1.39/lb",
      restock_days: ["Wednesday", "Saturday"],
      description: "Charlotte's busiest SA outlet in the West End. Large store with bins organized by category — easy to navigate for first-timers.",
      features: ["Clothing", "Housewares", "Toys", "Electronics", "Books"],
      verified: true, added: "2025-01-08"
    }

  ] /* end stores */

}; /* end SAData */
