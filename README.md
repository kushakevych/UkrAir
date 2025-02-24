# UkrAir


## Проектування архітектури бази даних

<img src="https://www.plantuml.com/plantuml/svg/dPLHJzim4CVVyocilW0JbO2fUvWG8Yj1gqOxLjAzHjVcMYmSkphRL8potUSuRXQQ5atbXKj-Pz__Vxwurze06Lk82ANXveLr9Xgfmq2pCc2l4ND_dwpbEVlA-j_ZyV7dBoViylB-nzMLPzsk_pVdf4qceK2NzpiU-zJUsOc70lQp9MYzLEIuBQP8ZOoBixBGP3JuDKb2CIo0YqRA-Lahns-uKfGtT-hrJgAtgFOOSofBUfiXtZZrFWUZr5iyPV4a_PaDHlrnCan6wNlBCvLZDeZJkEvCIqlmt9HRBNKoThvNLXhQYGmly8-IMotSSZKZc0TRuU40NuNp9VQNUK0mVG5Q-phrqm65zaq4yHbcXHM6BmNt8t6Jz0V3-EwuTthHqbBBE421HjWnUET1Y3PWh7OW6Ks6nqVm35p0LE3HAJiYr4ZFc9UnbVzGjH92zxE6bjlD5pChszKY3LTZPGrwMpuwmDTSyCMZqV_rJUMMm70bCyFzSQI3OL81UD6PccShnAVtMrGObq364kuq2KJy6SH7Dc-zIE-p2WymMelOgB-9qwHsGCgQFVB20NsaxvjIJrmklC0G7w1mQuYMA7EtKJasCoNdd0hC_GF86GeNXuk040pc6PXm8WzfFBptA2nhGJQQtDqrJd-dRusm6rYDb6rTydL7_4_1UjtjgjTD9rnYP-f2tOasRzvKjxjUXxCi-LnHYpuWU0PQyuN4l1E5_C3zn5UBXL0hlSthUysbECsE-nq3hM-Z4Zz2JTjhfoYKN6XcL2VoDHj9IqMLVbB5Vbgkl4QPsqBy1G00" alt="ER Diagram" />

#### SQL проєкція

```SQL
CREATE DATABASE flight_booking;
USE flight_booking;

CREATE TABLE USER (
    uuid CHAR(36) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE AIRPORTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code_IATA CHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE Aircrafts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(50) NOT NULL
);

CREATE TABLE SeatClasses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price_multiplier DECIMAL(5,2) NOT NULL
);

CREATE TABLE Seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aircraft_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    class_id INT NOT NULL,
    status ENUM('available', 'reserved', 'unavailable') NOT NULL,
    FOREIGN KEY (aircraft_id) REFERENCES Aircrafts(id),
    FOREIGN KEY (class_id) REFERENCES SeatClasses(id)
);

CREATE TABLE Routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flights_number VARCHAR(20) UNIQUE NOT NULL,
    departure_id INT NOT NULL,
    arrival_id INT NOT NULL,
    duration_time TIME NOT NULL,
    days_of_week VARCHAR(20) NOT NULL,
    FOREIGN KEY (departure_id) REFERENCES AIRPORTS(id),
    FOREIGN KEY (arrival_id) REFERENCES AIRPORTS(id)
);

CREATE TABLE FLIGHTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id INT NOT NULL,
    aircraft_id INT NOT NULL,
    departure_time DATETIME NOT NULL,
    FOREIGN KEY (route_id) REFERENCES Routes(id),
    FOREIGN KEY (aircraft_id) REFERENCES Aircrafts(id)
);

CREATE TABLE Booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT NOT NULL,
    seat_id INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    status ENUM('pending', 'confirmed', 'canceled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (flight_id) REFERENCES FLIGHTS(id),
    FOREIGN KEY (seat_id) REFERENCES Seats(id),
    FOREIGN KEY (user_id) REFERENCES USER(uuid)
);
```