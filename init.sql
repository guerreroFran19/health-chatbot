CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(20) CHECK (type IN ('appointment','medication')),
    title VARCHAR(150) NOT NULL,
    event_date TIMESTAMP NOT NULL,
    details TEXT,
    CONSTRAINT fk_event_user FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
