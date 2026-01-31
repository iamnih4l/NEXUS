# NexusGo
**Project Name:** NexusGo

**Problem Statement ID:** CS01SW

**Team Name:** NEXUS

**College Name:** SAHYADRI COLLEGE OF ENGINEERING AND MANAGEMENT

---

---

## Problem Statement

Large amounts of edible food are wasted daily by restaurants, events, and institutions, while NGOs and shelters struggle to meet the needs of vulnerable populations. Existing food donation systems are often manual, inefficient, and unreliable, lacking real-time coordination, trust assessment, spoilage awareness, and donor engagement. The problem is further complicated by uncertainty in food quality, human unreliability in pickups, logistical delays, and the ethical challenge of fair and consistent food redistribution.

---

## Proposed Solution

NexusGo is a digital, real-time food redistribution platform that intelligently connects surplus food sources with NGOs. The system uses an adaptive, trust-aware decision intelligence engine to dynamically allocate perishable food based on freshness, urgency, NGO reliability, logistics constraints, and ethical priorities.

To enhance food safety, NexusGo integrates an OpenCV-based food spoilage detection module that estimates freshness from food images and adjusts allocation urgency accordingly. Additionally, the platform introduces a streak-based donor reward system that incentivizes consistent food donations, encouraging long-term participation and reducing recurring food waste.

---

## Innovation & Creativity

- **Decision intelligence over simple matching:** Real-time, adaptive allocation instead of static donor–NGO pairing.
- **Trust-aware NGO scoring:** Reliability scores based on past pickups, timeliness, and feedback.
- **Ethical allocation logic:** Fairness and vulnerability are prioritized alongside urgency.
- **Computer vision integration:** OpenCV-based food spoilage detection to assess freshness and risk.
- **Streak-based donor rewards:** Gamified incentives that encourage consistent food donation behavior.
- **Adaptive reallocation:** Automatic reassignment when delays, failures, or uncertainty arise.
- **Agentic AI:** AI that transparently explains and justifies resource allocations to NGOs .


---

## Technical Complexity & Stack

**Frontend:**  
- React / Next.js  
- Tailwind CSS  

**Backend:**  
- Node.js / Express  
- REST APIs  

**AI & Decision Engine:**  
- Python  
- Multi-objective scoring and rule-based optimization  

**Computer Vision:**  
- OpenCV  
- Image preprocessing and spoilage classification  

**Database:**  
- MongoDB / Firebase  

**Gamification & Rewards:**  
- Streak tracking logic  
- Badge and reward scoring system  

**Other Tools:**  
- GitHub  
- Figma (UI/UX design)

---

## Usability & Impact

**Users:**  
- Food donors (restaurants, hotels, event organizers)  
- NGOs and shelters  
- Platform administrators  

**User Interaction:**  
- Donors upload surplus food details and images  
- NGOs receive real-time allocation requests  
- The system dynamically assigns, prioritizes, and reroutes food  
- Donors earn streaks and rewards for consistent contributions
- AI explains and justifies resource allocations to NGOs usingdata-driven reasoning and logical decision

**Real-World Impact:**  
- Reduced food waste  
- Faster and safer redistribution  
- Increased donor participation  
- Improved trust and accountability  
- Fair and ethical food distribution  

---

## Setup Instructions

### Prerequisites
- Node.js  
- Python 3.x  
- Git  

### Steps to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-repo/NexusGo.git

# Install frontend dependencies
cd frontend
npm install
npm run dev

# Install backend dependencies
cd backend
npm install
npm start

# Run OpenCV spoilage detection module
cd vision
python spoilage_detection.py
```
---
## Demo Link :  
- https://drive.google.com/file/d/1TY3BbFbmcah69i7jvLhzaphLuDYb7Rqz/view?usp=drive_link


---
