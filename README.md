# ⭐ Project STAR
### Real-Time Multiplayer Game Backend

🚀 Built a scalable backend system to simulate real-time multiplayer gameplay using a room-based architecture and state-driven game engine.

---

👥 Developed By  
- Dinesh  
- Jyothika  

---

## 📌 Overview

Project STAR is a multiplayer, turn-based card game backend designed to handle complete game flow including player management, identity selection, deck generation, turn-based gameplay, star race mechanics, score calculation, and multi-round progression.

---

## 🎯 Key Features

### 🏠 Room Management  
- Create and join rooms using unique room IDs  
- Host-controlled game flow  
- Automatic host transfer on player leave  
- Room deletion when empty  

### 🎭 Identity Selection  
- Unique identity selection per player  
- Duplicate validation and input normalization  
- Host-controlled forced identity allocation  

### 🎮 Game Flow Management  
- Lobby → Identity Selection → In Game → Star Race → Round Result → Game Over  
- Strict state validation across all transitions  

### 🃏 Deck Generation & Distribution  
- Dynamic deck generation based on player identities  
- Secret identity logic implementation  
- Shuffled deck for randomness  
- Card distribution:
  - Host → 5 cards  
  - Others → 4 cards  

### 🔄 Turn-Based Gameplay  
- Circular turn system using index-based logic  
- Card passing via index selection  
- Turn ownership validation  
- Winner detection based on card conditions  

### ⭐ Star Race System  
- Triggered after winner detection  
- Ordered player participation  
- Duplicate participation prevention  
- Host-controlled completion  

### 🧮 Scoring System  
- Winner → +1000 points  
- Star race ranking → +900, +800, +700...  
- Secret card bonus → +100  
- Round-wise and cumulative score tracking  

### 🔁 Multi-Round Support  
- Configurable rounds (3 / 5 / 7)  
- Round-wise score tracking  
- Automatic game progression  
- Final winner determination  

### 📊 Game State API  
- Real-time room state tracking  
- Player card count visibility  
- Current turn tracking  
- Score snapshots and round results  

---

## 🏗️ Architecture

The project follows a clean layered architecture:

API Layer (views.py)  
↓  
Service / Storage Layer (storage.py)  
↓  
Game Logic Layer (room.py / player.py)  

Each layer is responsible for:

- API Layer → Handles HTTP requests and responses  
- Storage Layer → Manages room instances and acts as a mediator  
- Game Logic Layer → Contains core game rules and state transitions  

---

## 🧠 Engineering Highlights

- State-driven game flow management  
- Circular turn handling using index-based logic  
- Efficient player lookup using dictionary mapping  
- Strong validation and error handling  
- Clean separation of concerns  

---

## 🧪 Testing

- End-to-end game flow tested using Postman  
- Simulated multiple players interacting in real-time  
- Validated edge cases and error handling  
- Verified state transitions across all gameplay phases  

---

## 🛠️ Tech Stack

- Python  
- Django  
- Django REST Framework  
- In-memory data management  
- Postman (API testing)  

---

## 🚀 Future Enhancements

- Frontend integration (React)  
- Real-time gameplay using WebSockets  
- Database integration (PostgreSQL)  
- Authentication system  
- Game analytics dashboard  

---

## 📌 Conclusion

Project STAR demonstrates strong backend engineering skills including system design, state management, and real-time game logic implementation.

Built with a focus on scalability, consistency, and clean architecture.

---

⭐ If you like this project, feel free to star the repository!
