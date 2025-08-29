


Capstone project for the **IBM Data Science Professional Certificate**.  
We analyze SpaceX Falcon 9 launch data and build ML models to **predict first-stage landing success**—a key driver of launch cost via reuse.

---

## 📌 Executive Summary

- **Objective:** Predict first-stage landing to support cost planning and mission design.
- **Approach:** SpaceX API + Wikipedia scraping → wrangling/feature engineering → EDA (SQL + visuals) → interactive analytics (Folium map, Plotly Dash) → ML (LR, SVM, DT, KNN) with GridSearchCV.
- **Key Results (from the project runs):**
  - **Best model (CV): Decision Tree**, CV accuracy ≈ **0.875**, **Test accuracy ≈ 0.8889**.
  - Logistic Regression — CV ≈ **0.8464**, **Test ≈ 0.8333**.
  - SVM — **best kernel: sigmoid**, CV ≈ **0.8482**.
  - KNN — **k=10, p=1**, CV ≈ **0.8482**.
  - Landing success varies by **launch site, orbit, and payload**; success improves over time.
- **Recommendation:** Use the model pre-launch to select higher-probability configurations; extend features (weather/trajectory) for improved accuracy.

---

## 🌐 Data Sources

- **SpaceX REST API v4**  
  - Base: `/launches/past`  
  - Lookups: `/rockets`, `/payloads`, `/launchpads`, `/cores` (to resolve IDs)
- **Wikipedia**  
  - *List of Falcon 9 and Falcon Heavy launches* (HTML tables scraped with BeautifulSoup)

---
## 🔬 Methodology

### 1) Collection
- `requests.get(...).json()` → `pandas.json_normalize()` for launch records.  
- **Resolved IDs** via rockets/payloads/launchpads/cores endpoints.  
- **Web scraping** of Wikipedia tables (BeautifulSoup) to enrich/verify payload, orbit, outcome.

### 2) Wrangling
- Filtered to **Falcon 9** launches; kept **single core** and **single payload** rows.
- Converted `date_utc` → date; restricted to dates **≤ 2020-11-13**.
- **Imputation:** `PayloadMass` missing values filled with mean; `LandingPad=None` retained for one-hot encoding later.
- Created clean tabular datasets (`dataset_part_1.csv`, plus modeling parts).

### 3) EDA (Pandas + SQL)
- **SQL (SQLite)** examples:
  - Unique launch sites; CCAFS SLC-40 **launches = 13**.
  - Success rate example: **~67%** (by site query).
  - Geosynchronous orbit (GTO) **count = 27**.
  - Mission outcome “**True ASDS**” (successful drone ship landings) **= 41**.
- **Visual EDA:** site distributions, orbit distribution, payload vs success, yearly trend.

### 4) Interactive Visual Analytics
- **Folium map:** launch site markers; success/failure colored markers with `MarkerCluster`.
- Proximity distances (Haversine) from **KSC LC-39A** to:
  - Coastline: **~7.19 km**
  - Nearby highway (State Road 3): **~7.70 km**
  - Nearby railway (Indian River RR): **~20.43 km**
  - Orlando (city center approx.): **~67.56 km**

### 5) Modeling
- Feature set included: `FlightNumber, PayloadMass, Orbit, LaunchSite, Flights, GridFins, Reused, Legs, LandingPad, Block, ReusedCount, Serial`.
- **One-hot encoding** for categoricals; **StandardScaler** for numerics.
- **Train/Test split:** 80/20, `random_state=2`.
- **GridSearchCV (cv=10)** across:
  - Logistic Regression (`C`, `solver`, `penalty=l2`)
  - SVM (`kernel`, `C`, `gamma`) → **best kernel: sigmoid**
  - Decision Tree (`criterion`, `splitter`, `max_depth`, `max_features`, `min_samples_*`)
  - KNN (`n_neighbors`, `p`, `algorithm`)

---

## 📊 Key Findings

- **By Site:** Success ratios differ (e.g., **KSC LC-39A** and **VAFB SLC-4E** higher; **CCAFS LC-40** lower).
- **By Orbit:** Counts observed (example) — **GTO=27, ISS=21, VLEO=14, PO=9, LEO=7, SSO=5, MEO=3, HEO=1, ES-L1=1, SO=1, GEO=1**.
- **Mission Outcomes (sample counts):**
  - **True ASDS=41**, **True RTLS=14**, **False ASDS=6**, **True Ocean=5**, **False Ocean=2**, **None ASDS=2**, **False RTLS=1**, **None None=19**.
- **Trend:** Success improved notably after ~2017.
- **Dash insights:** Payload bands and site filters reveal clear patterns in success likelihood.

---

## 🗺️ Interactive Visual Analytics

- **Folium:** Interactive site map; colored markers for success/failure; proximity lines/labels.  
- **Plotly Dash:**
  - **Dropdown:** select launch site (All/Site-specific).
  - **Range slider:** filter by payload mass.
  - **Pie chart:** success counts (All) or success vs failure for selected site.
  - **Scatter:** payload vs class, colored by Booster Version Category.

---

## 🤖 Machine Learning Results

- **Logistic Regression:**  
  - **CV ≈ 0.8464**, **Test ≈ 0.8333**
- **Support Vector Machine (SVM):**  
  - **Best kernel: sigmoid**, **CV ≈ 0.8482**
- **Decision Tree (BEST):**  
  - **CV ≈ 0.875**, **Test ≈ 0.8889**
- **K-Nearest Neighbors (KNN):**  
  - **k = 10**, **p = 1**, **CV ≈ 0.8482**

*Confusion matrices (e.g., Logistic Regression) show some false positives (predict “land” when it didn’t), which should be considered in operational use.*

---

## ▶️ How to Run

> Ensure you have Python 3.9+ (works with 3.11 as used in the lab).

### 1) Create a virtual environment & install dependencies
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
